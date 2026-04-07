# Incident Channel Summarizer - Quick Reference

## Quick Start Commands

```bash
# 1. Test configuration
python3 test_config.py

# 2. Run summarizer
./run_summarizer.sh
```

## Environment Variables

```bash
export SLACK_BOT_TOKEN="xoxb-..."
export CONFLUENCE_USERNAME="you@nestoca.ca"
export CONFLUENCE_API_TOKEN="..."
export CONFLUENCE_URL="https://nestoca.atlassian.net"
```

## Required Slack Scopes

- `channels:history` - Read public channel messages
- `groups:history` - Read private channel messages
- `users:read` - Get user information
- `channels:read` - View channel info
- `groups:read` - View private channel info

## Common Error Solutions

| Error | Solution |
|-------|----------|
| Channel not found | Invite bot: `/invite @BotName` |
| 401 Unauthorized | Check token validity, regenerate if needed |
| 403 Forbidden | Verify OAuth scopes, reinstall app |
| Missing scope | Add scope in Slack app settings, reinstall |
| Confluence 401 | Verify username and API token |
| Confluence 403 | Check page edit permissions |
| Module not found | Run `pip install -r requirements.txt` |
| Rate limit | Wait and retry, reduce request frequency |

## File Structure

```
.
├── incident_channel_summarizer.py  # Main script
├── test_config.py                  # Configuration tester
├── run_summarizer.sh              # Shell wrapper
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── INCIDENT_SUMMARIZER_README.md  # Full documentation
├── SETUP_GUIDE.md                 # Step-by-step setup
└── QUICK_REFERENCE.md             # This file
```

## Customization Points

### Change Target Channel
Edit `incident_channel_summarizer.py` line 265:
```python
CHANNEL_NAME = "your-channel-name"
```

### Change Target Page
Edit `incident_channel_summarizer.py` line 268:
```python
CONFLUENCE_PAGE_ID = "your-page-id"
```

### Replace Instead of Append
Edit `incident_channel_summarizer.py` line 271:
```python
summarizer.run(CHANNEL_NAME, CONFLUENCE_PAGE_ID, append=False)
```

## Finding Confluence Page ID

From the URL:
```
https://nestoca.atlassian.net/wiki/spaces/CS/pages/5055152132/Page+Title
                                                      ^^^^^^^^^^ This is the ID
```

## Output Categories

Actions are automatically categorized as:
- **Investigation** - investigated, checked, reviewed, analyzed, found
- **Remediation** - deployed, updated, patched, fixed, reverted
- **Monitoring** - monitoring, watching, tracking, observing
- **Communication** - notified, informed, communicated, alerted
- **Mitigation** - blocked, disabled, restricted, prevented
- **Other** - Everything else

## Getting Help

1. Run configuration test: `python3 test_config.py`
2. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
3. Review [INCIDENT_SUMMARIZER_README.md](INCIDENT_SUMMARIZER_README.md) for troubleshooting
4. Check Slack API docs: https://api.slack.com/docs
5. Check Confluence API docs: https://developer.atlassian.com/cloud/confluence/

## Security Checklist

- [ ] Never commit `.env` file
- [ ] Use `.env.example` as template
- [ ] Store tokens in secret management (Cursor secrets for cloud agents)
- [ ] Use minimum required OAuth scopes
- [ ] Rotate tokens regularly
- [ ] Revoke tokens immediately if compromised

## Performance Notes

- Fetches up to 200 messages per API call
- Pagination handles channels of any size
- Rate limits: ~50 requests/minute for Slack
- Processing time: ~1-2 seconds per 100 messages
- Confluence update: Single request regardless of content size

## Integration with Cursor Cloud Agents

Add secrets at: **Cursor Dashboard → Cloud Agents → Secrets**

| Secret Key | Example Value |
|------------|---------------|
| SLACK_BOT_TOKEN | xoxb-1234567890-... |
| CONFLUENCE_USERNAME | engineer@nestoca.ca |
| CONFLUENCE_API_TOKEN | ATATT3xFf... |
| CONFLUENCE_URL | https://nestoca.atlassian.net |

Secrets are automatically injected as environment variables.

## Example Workflow

1. **Incident Occurs**
   - Team responds in `#incident-xxx` channel
   - Actions, links, and decisions are discussed

2. **Post-Incident**
   - Set environment variables or configure secrets
   - Run `python3 test_config.py` to verify setup
   - Run `./run_summarizer.sh` to generate summary

3. **Documentation**
   - Confluence page is automatically updated
   - Summary includes all team actions, timestamps, and links
   - Ready for post-incident review

## Time Estimates

| Task | Time |
|------|------|
| Initial setup (first time) | 15-20 minutes |
| Configuration test | 10-15 seconds |
| Running summarizer (100 messages) | 5-10 seconds |
| Running summarizer (1000 messages) | 30-45 seconds |

## Support Channels

- For tool issues: Check documentation files
- For Slack API issues: https://api.slack.com/support
- For Confluence issues: https://support.atlassian.com

---

**Version**: 1.0  
**Last Updated**: 2026-04-07  
**Maintained by**: nesto.ca Engineering
