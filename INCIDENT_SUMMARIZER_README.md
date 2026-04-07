# Incident Channel Summarizer

This tool fetches messages from a Slack incident channel and creates a comprehensive summary on a Confluence wiki page, organized by team member and action type.

## Features

- Fetches complete channel history from Slack
- Organizes actions by user with their roles/titles
- Categorizes actions (Investigation, Remediation, Monitoring, Communication, Mitigation, Other)
- Extracts and lists all links/queries mentioned
- Updates Confluence wiki page with formatted summary
- Timestamps all actions for timeline reconstruction

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

You need to set up the following environment variables:

#### Slack Configuration

Get a Slack Bot Token from your Slack workspace:
1. Go to https://api.slack.com/apps
2. Create or select your app
3. Navigate to "OAuth & Permissions"
4. Add required scopes:
   - `channels:history` (for public channels)
   - `groups:history` (for private channels)
   - `users:read` (to get user information)
   - `conversations.list` (to find channels)
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

Set the token:
```bash
export SLACK_BOT_TOKEN="xoxb-your-token-here"
# OR
export SLACK_TOKEN="xoxb-your-token-here"
```

#### Confluence Configuration

Get Confluence API credentials:
1. Log in to Confluence
2. Go to https://id.atlassian.com/manage-profile/security/api-tokens
3. Create an API token
4. Use your Atlassian email as username

Set the credentials:
```bash
export CONFLUENCE_USERNAME="your-email@nestoca.ca"
export CONFLUENCE_API_TOKEN="your-api-token"
export CONFLUENCE_URL="https://nestoca.atlassian.net"  # Optional, this is the default
```

### 3. Run the Script

```bash
python incident_channel_summarizer.py
```

## How It Works

1. **Channel Discovery**: Finds the Slack channel by name
2. **Message Retrieval**: Fetches all messages using pagination
3. **User Identification**: Retrieves user names and roles
4. **Action Categorization**: Analyzes message content to categorize actions
5. **Link Extraction**: Finds all URLs and references
6. **Summary Generation**: Creates structured HTML content
7. **Confluence Update**: Appends summary to the specified wiki page

## Output Format

The Confluence page will include:

- **Header**: Channel name, generation timestamp, message count
- **Actions by Team Member**: Grouped by user, showing:
  - Name and title/role
  - Action count
  - Actions organized by category with timestamps
  - Links referenced in each action
- **All Links Section**: Complete list of all URLs mentioned

## Customization

Edit `incident_channel_summarizer.py` to customize:

- **Channel Name**: Line 265 - `CHANNEL_NAME`
- **Confluence Page ID**: Line 268 - `CONFLUENCE_PAGE_ID`
- **Append vs Replace**: Line 271 - `append=True` (set to `False` to replace content)
- **Action Categories**: Method `categorize_action()` - add keywords for better categorization
- **Message Filtering**: Method `summarize_channel()` - adjust message length threshold

## Using with Cursor Cloud Agents

To use this in Cursor's Cloud Agent environment, ensure secrets are configured:

1. Go to Cursor Dashboard → Cloud Agents → Secrets
2. Add the following secrets:
   - `SLACK_BOT_TOKEN`
   - `CONFLUENCE_USERNAME`
   - `CONFLUENCE_API_TOKEN`
   - `CONFLUENCE_URL` (optional)

These will be automatically injected as environment variables when the agent runs.

## Troubleshooting

### "Channel not found"
- Ensure the bot is added to the channel (`/invite @YourBot`)
- Check that the channel name is correct (without #)
- Verify the bot has appropriate permissions

### "Error fetching channel history"
- Confirm the bot token has the required scopes
- Check if the channel is private and bot has access
- Verify rate limits aren't exceeded

### "Error updating Confluence page"
- Verify the page ID is correct (from the URL)
- Ensure API token is valid and not expired
- Check that the user has edit permissions on the page
- Confirm the Confluence URL is correct

### "Configuration Error"
- Double-check all environment variables are set
- Ensure there are no extra spaces in the values
- Verify the tokens haven't expired

## Example Output

The summary will look like this on Confluence:

---

## Incident Channel Summary: #incident-security-axios-compromised-on-npm

*Generated: 2026-04-07 14:30:00 UTC*

**Total Messages Analyzed:** 47

### Actions Taken by Team Members

#### John Doe *(Senior Security Engineer)*
**Actions: 12**

**Investigation:**
- *[2026-04-07 10:15:23 UTC]* Investigated the axios package on npm registry...
  **Links:** https://www.npmjs.com/package/axios

**Remediation:**
- *[2026-04-07 10:45:12 UTC]* Deployed patch to production blocking axios 1.6.x...

---

## License

Internal use only - nesto.ca
