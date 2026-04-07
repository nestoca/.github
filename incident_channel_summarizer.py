#!/usr/bin/env python3
"""
Slack Incident Channel Summarizer
Fetches messages from a Slack incident channel and updates a Confluence wiki page
with a summary of actions taken, organized by user and role.
"""

import os
import sys
from datetime import datetime
from collections import defaultdict
import re
from typing import List, Dict, Any

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from atlassian import Confluence


class IncidentChannelSummarizer:
    def __init__(self):
        # Initialize Slack client
        self.slack_token = os.getenv('SLACK_BOT_TOKEN') or os.getenv('SLACK_TOKEN')
        if not self.slack_token:
            raise ValueError("SLACK_BOT_TOKEN or SLACK_TOKEN environment variable is required")
        
        self.slack_client = WebClient(token=self.slack_token)
        
        # Initialize Confluence client
        self.confluence_url = os.getenv('CONFLUENCE_URL', 'https://nestoca.atlassian.net')
        self.confluence_username = os.getenv('CONFLUENCE_USERNAME')
        self.confluence_token = os.getenv('CONFLUENCE_API_TOKEN')
        
        if not self.confluence_username or not self.confluence_token:
            raise ValueError("CONFLUENCE_USERNAME and CONFLUENCE_API_TOKEN environment variables are required")
        
        self.confluence = Confluence(
            url=self.confluence_url,
            username=self.confluence_username,
            password=self.confluence_token,
            cloud=True
        )
    
    def get_channel_id(self, channel_name: str) -> str:
        """Get channel ID from channel name."""
        try:
            # Remove # if present
            channel_name = channel_name.lstrip('#')
            
            # Try to get channel info directly
            response = self.slack_client.conversations_list(
                types="public_channel,private_channel",
                limit=1000
            )
            
            for channel in response['channels']:
                if channel['name'] == channel_name:
                    return channel['id']
            
            raise ValueError(f"Channel '{channel_name}' not found")
        
        except SlackApiError as e:
            raise Exception(f"Error fetching channel ID: {e.response['error']}")
    
    def fetch_channel_history(self, channel_id: str) -> List[Dict[str, Any]]:
        """Fetch all messages from a channel."""
        messages = []
        cursor = None
        
        try:
            while True:
                response = self.slack_client.conversations_history(
                    channel=channel_id,
                    cursor=cursor,
                    limit=200
                )
                
                messages.extend(response['messages'])
                
                if not response.get('has_more'):
                    break
                
                cursor = response['response_metadata']['next_cursor']
            
            # Sort messages chronologically (oldest first)
            messages.sort(key=lambda x: float(x['ts']))
            
            return messages
        
        except SlackApiError as e:
            raise Exception(f"Error fetching channel history: {e.response['error']}")
    
    def get_user_info(self, user_id: str) -> Dict[str, str]:
        """Get user information from Slack."""
        try:
            response = self.slack_client.users_info(user=user_id)
            user = response['user']
            
            return {
                'name': user.get('real_name', user.get('name', 'Unknown')),
                'display_name': user.get('profile', {}).get('display_name', ''),
                'title': user.get('profile', {}).get('title', 'N/A')
            }
        except SlackApiError:
            return {
                'name': f'User {user_id}',
                'display_name': '',
                'title': 'N/A'
            }
    
    def extract_links(self, text: str) -> List[str]:
        """Extract URLs from message text."""
        # Slack format: <url|text> or <url>
        slack_links = re.findall(r'<([^|>]+)(?:\|[^>]+)?>', text)
        # Regular URLs
        regular_links = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
        
        return list(set(slack_links + regular_links))
    
    def categorize_action(self, text: str) -> str:
        """Categorize the type of action based on message content."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['investigated', 'checked', 'reviewed', 'analyzed', 'found']):
            return 'Investigation'
        elif any(word in text_lower for word in ['deployed', 'updated', 'patched', 'fixed', 'reverted']):
            return 'Remediation'
        elif any(word in text_lower for word in ['monitoring', 'watching', 'tracking', 'observing']):
            return 'Monitoring'
        elif any(word in text_lower for word in ['notified', 'informed', 'communicated', 'alerted']):
            return 'Communication'
        elif any(word in text_lower for word in ['blocked', 'disabled', 'restricted', 'prevented']):
            return 'Mitigation'
        else:
            return 'Other'
    
    def summarize_channel(self, channel_name: str) -> Dict[str, Any]:
        """Create a summary of actions taken in the channel."""
        channel_id = self.get_channel_id(channel_name)
        messages = self.fetch_channel_history(channel_id)
        
        # Group actions by user
        actions_by_user = defaultdict(list)
        all_links = []
        user_info_cache = {}
        
        for msg in messages:
            # Skip bot messages and system messages
            if msg.get('subtype') in ['channel_join', 'channel_leave', 'channel_topic', 'channel_purpose']:
                continue
            
            user_id = msg.get('user')
            if not user_id:
                continue
            
            text = msg.get('text', '')
            if not text or len(text.strip()) < 10:
                continue
            
            # Get user info
            if user_id not in user_info_cache:
                user_info_cache[user_id] = self.get_user_info(user_id)
            
            user_info = user_info_cache[user_id]
            timestamp = datetime.fromtimestamp(float(msg['ts'])).strftime('%Y-%m-%d %H:%M:%S UTC')
            
            # Extract links
            links = self.extract_links(text)
            all_links.extend(links)
            
            # Categorize action
            category = self.categorize_action(text)
            
            # Create action entry
            action = {
                'timestamp': timestamp,
                'text': text,
                'links': links,
                'category': category
            }
            
            actions_by_user[user_id].append(action)
        
        # Create summary structure
        summary = {
            'channel_name': channel_name,
            'total_messages': len(messages),
            'users': {},
            'all_links': list(set(all_links)),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        
        for user_id, actions in actions_by_user.items():
            user_info = user_info_cache[user_id]
            summary['users'][user_id] = {
                'name': user_info['name'],
                'title': user_info['title'],
                'actions': actions,
                'action_count': len(actions)
            }
        
        return summary
    
    def format_confluence_content(self, summary: Dict[str, Any]) -> str:
        """Format the summary as Confluence Storage Format (HTML)."""
        html_parts = []
        
        # Header
        html_parts.append(f"<h2>Incident Channel Summary: #{summary['channel_name']}</h2>")
        html_parts.append(f"<p><em>Generated: {summary['generated_at']}</em></p>")
        html_parts.append(f"<p><strong>Total Messages Analyzed:</strong> {summary['total_messages']}</p>")
        
        # Actions by User
        html_parts.append("<h3>Actions Taken by Team Members</h3>")
        
        # Sort users by action count (descending)
        sorted_users = sorted(
            summary['users'].items(),
            key=lambda x: x[1]['action_count'],
            reverse=True
        )
        
        for user_id, user_data in sorted_users:
            html_parts.append(f"<h4>{user_data['name']}")
            if user_data['title'] != 'N/A':
                html_parts.append(f" <em>({user_data['title']})</em>")
            html_parts.append(f"</h4>")
            html_parts.append(f"<p><strong>Actions: {user_data['action_count']}</strong></p>")
            
            # Group actions by category
            actions_by_category = defaultdict(list)
            for action in user_data['actions']:
                actions_by_category[action['category']].append(action)
            
            for category, actions in sorted(actions_by_category.items()):
                html_parts.append(f"<p><strong>{category}:</strong></p>")
                html_parts.append("<ul>")
                
                for action in actions:
                    html_parts.append(f"<li>")
                    html_parts.append(f"<em>[{action['timestamp']}]</em> ")
                    
                    # Truncate long messages
                    text = action['text']
                    if len(text) > 300:
                        text = text[:297] + "..."
                    
                    # Escape HTML entities
                    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    html_parts.append(text)
                    
                    if action['links']:
                        html_parts.append("<br/><strong>Links:</strong> ")
                        for link in action['links']:
                            html_parts.append(f'<a href="{link}">{link}</a> ')
                    
                    html_parts.append("</li>")
                
                html_parts.append("</ul>")
        
        # All Links Section
        if summary['all_links']:
            html_parts.append("<h3>All Links Referenced</h3>")
            html_parts.append("<ul>")
            for link in sorted(set(summary['all_links'])):
                html_parts.append(f'<li><a href="{link}">{link}</a></li>')
            html_parts.append("</ul>")
        
        return ''.join(html_parts)
    
    def update_confluence_page(self, page_id: str, new_content: str, append: bool = True):
        """Update a Confluence page with the summary."""
        try:
            # Get current page
            page = self.confluence.get_page_by_id(
                page_id=page_id,
                expand='body.storage,version'
            )
            
            current_content = page['body']['storage']['value']
            current_version = page['version']['number']
            
            # Prepare new content
            if append:
                # Add separator and new content
                separator = "<hr/><h2>Incident Summary Update</h2>"
                final_content = current_content + separator + new_content
            else:
                final_content = new_content
            
            # Update page
            self.confluence.update_page(
                page_id=page_id,
                title=page['title'],
                body=final_content,
                parent_id=page.get('ancestors', [{}])[-1].get('id') if page.get('ancestors') else None,
                type='page',
                representation='storage',
                minor_edit=False
            )
            
            print(f"Successfully updated Confluence page: {page['title']}")
            
        except Exception as e:
            raise Exception(f"Error updating Confluence page: {str(e)}")
    
    def run(self, channel_name: str, confluence_page_id: str, append: bool = True):
        """Main execution method."""
        print(f"Fetching history from channel: #{channel_name}")
        summary = self.summarize_channel(channel_name)
        
        print(f"\nFound {len(summary['users'])} users with actions")
        print(f"Total links referenced: {len(summary['all_links'])}")
        
        print("\nFormatting content for Confluence...")
        confluence_content = self.format_confluence_content(summary)
        
        print(f"\nUpdating Confluence page ID: {confluence_page_id}")
        self.update_confluence_page(confluence_page_id, confluence_content, append)
        
        print("\n✅ Summary complete!")
        
        return summary


def main():
    # Configuration
    CHANNEL_NAME = "incident-security-axios-compromised-on-npm"
    
    # Extract page ID from URL: https://nestoca.atlassian.net/wiki/spaces/CS/pages/5055152132/...
    CONFLUENCE_PAGE_ID = "5055152132"
    
    try:
        summarizer = IncidentChannelSummarizer()
        summarizer.run(CHANNEL_NAME, CONFLUENCE_PAGE_ID, append=True)
    
    except ValueError as e:
        print(f"❌ Configuration Error: {e}", file=sys.stderr)
        print("\nRequired environment variables:", file=sys.stderr)
        print("  - SLACK_BOT_TOKEN or SLACK_TOKEN", file=sys.stderr)
        print("  - CONFLUENCE_USERNAME", file=sys.stderr)
        print("  - CONFLUENCE_API_TOKEN", file=sys.stderr)
        print("  - CONFLUENCE_URL (optional, defaults to https://nestoca.atlassian.net)", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
