# Setup Guide for Incident Channel Summarizer

This guide walks you through setting up the required credentials and running the summarizer.

## Prerequisites

- Access to the Slack workspace with the incident channel
- Atlassian/Confluence account with edit permissions on the target wiki page
- Python 3.7+ installed

## Step 1: Create Slack Bot

### 1.1 Create a Slack App
1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. Choose "From scratch"
4. Name: "Incident Summarizer"
5. Select your workspace

### 1.2 Configure Bot Permissions
1. In your app settings, go to "OAuth & Permissions"
2. Scroll to "Scopes" → "Bot Token Scopes"
3. Add the following scopes:
   - `channels:history` - Read messages in public channels
   - `groups:history` - Read messages in private channels
   - `users:read` - View people in the workspace
   - `channels:read` - View basic channel info
   - `groups:read` - View basic private channel info

### 1.3 Install App to Workspace
1. Scroll to top of "OAuth & Permissions" page
2. Click "Install to Workspace"
3. Review permissions and click "Allow"
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`)
5. Save this token securely

### 1.4 Add Bot to Incident Channel
1. Go to the incident channel in Slack
2. Type: `/invite @Incident Summarizer`
3. The bot must be in the channel to read history

## Step 2: Get Confluence API Token

### 2.1 Create API Token
1. Log in to your Atlassian account
2. Go to https://id.atlassian.com/manage-profile/security/api-tokens
3. Click "Create API token"
4. Name: "Incident Summarizer"
5. Copy the token (you won't see it again!)

### 2.2 Note Your Confluence Details
- Username: Your Atlassian email address
- URL: Your Confluence instance URL (e.g., https://nestoca.atlassian.net)

## Step 3: Configure Environment Variables

### Option A: Using .env file (Local Development)
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Add your credentials:
```env
SLACK_BOT_TOKEN=xoxb-your-actual-token-here
CONFLUENCE_USERNAME=your.email@nestoca.ca
CONFLUENCE_API_TOKEN=your-actual-confluence-token
CONFLUENCE_URL=https://nestoca.atlassian.net
```

Then load the variables:
```bash
source .env  # or export them manually
```

### Option B: Cursor Cloud Agents
1. Go to https://cursor.com/settings
2. Navigate to "Cloud Agents" → "Secrets"
3. Add these secrets:
   - Key: `SLACK_BOT_TOKEN`, Value: `xoxb-...`
   - Key: `CONFLUENCE_USERNAME`, Value: `your.email@nestoca.ca`
   - Key: `CONFLUENCE_API_TOKEN`, Value: `your-token`
   - Key: `CONFLUENCE_URL`, Value: `https://nestoca.atlassian.net`

### Option C: Direct Export (Temporary)
```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export CONFLUENCE_USERNAME="your.email@nestoca.ca"
export CONFLUENCE_API_TOKEN="your-token"
export CONFLUENCE_URL="https://nestoca.atlassian.net"
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Or with a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 5: Configure Target Channel and Page

Edit `incident_channel_summarizer.py` to set:

```python
# Line 265 - Channel name (without #)
CHANNEL_NAME = "incident-security-axios-compromised-on-npm"

# Line 268 - Confluence page ID (from URL)
CONFLUENCE_PAGE_ID = "5055152132"
```

### How to Find Confluence Page ID
From the URL:
```
https://nestoca.atlassian.net/wiki/spaces/CS/pages/5055152132/Playbook+Title
                                                      ^^^^^^^^^^ This is the page ID
```

## Step 6: Run the Summarizer

### Using the Shell Wrapper
```bash
./run_summarizer.sh
```

### Direct Python Execution
```bash
python3 incident_channel_summarizer.py
```

## Expected Output

```
🔍 Incident Channel Summarizer
================================

✅ Configuration validated
🚀 Running summarizer...

Fetching history from channel: #incident-security-axios-compromised-on-npm

Found 5 users with actions
Total links referenced: 23

Formatting content for Confluence...

Updating Confluence page ID: 5055152132
Successfully updated Confluence page: Playbook: Open-source Supply-chain Compromise

✅ Summary complete!
```

## Troubleshooting

### "Channel not found"
**Solution**: 
- Verify channel name is correct (case-sensitive)
- Ensure bot is invited to the channel: `/invite @Incident Summarizer`
- Check bot has `channels:read` or `groups:read` scope

### "Not enough permissions"
**Solution**:
- Re-check OAuth scopes in Slack app settings
- Reinstall the app to workspace after adding scopes
- Verify bot is a member of the channel

### "Error updating Confluence page"
**Solution**:
- Verify page ID is correct
- Check Confluence credentials are valid
- Ensure your user has edit permissions on the page
- Try accessing the page manually in a browser

### "Module not found"
**Solution**:
```bash
pip install -r requirements.txt
```

### "401 Unauthorized" (Confluence)
**Solution**:
- Verify API token is correct and not expired
- Check username is your Atlassian email
- Ensure URL doesn't have trailing slash

### "403 Forbidden" (Slack)
**Solution**:
- Bot token might be invalid
- Reinstall app and get new token
- Check workspace hasn't revoked app access

## Verification

After running, verify the summary by:
1. Opening the Confluence page in your browser
2. Scrolling to the bottom to see the new summary
3. Checking that:
   - All team members are listed
   - Actions are properly categorized
   - Timestamps are correct
   - Links are properly formatted and clickable

## Customization

### Change Channel or Page
Edit these lines in `incident_channel_summarizer.py`:
```python
CHANNEL_NAME = "your-channel-name"
CONFLUENCE_PAGE_ID = "your-page-id"
```

### Replace Instead of Append
Change line 271:
```python
summarizer.run(CHANNEL_NAME, CONFLUENCE_PAGE_ID, append=False)
```

### Adjust Action Categories
Modify the `categorize_action()` method to add keywords:
```python
def categorize_action(self, text: str) -> str:
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['your', 'keywords', 'here']):
        return 'Your Category'
    # ... rest of categories
```

## Security Best Practices

1. Never commit `.env` file to git (already in `.gitignore`)
2. Rotate API tokens regularly
3. Use bot tokens with minimum required scopes
4. Store tokens in secure secret management systems
5. Revoke tokens immediately if compromised

## Support

For issues or questions:
- Check the [main documentation](./INCIDENT_SUMMARIZER_README.md)
- Review Slack API docs: https://api.slack.com/docs
- Review Confluence API docs: https://developer.atlassian.com/cloud/confluence/rest/

## Next Steps

After successful execution:
1. Review the Confluence summary for accuracy
2. Consider running for other incident channels
3. Set up as a scheduled job if needed
4. Share the tool with your incident response team
