# Documentation Index

Welcome to the Incident Channel Summarizer documentation! This index helps you find the right documentation for your needs.

## 📚 Documentation Files

### Quick Start

**[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - 2 minutes  
For users who've already set up the tool and need quick access to commands or troubleshooting.

**What's inside:**
- Common commands
- Environment variables reference
- Error solutions table
- File structure overview
- Key customization points

**Best for:** Repeat users, quick lookups, common errors

---

### Feature Overview

**[INCIDENT_SUMMARIZER_README.md](./INCIDENT_SUMMARIZER_README.md)** - 10 minutes  
Comprehensive overview of features, capabilities, and use cases.

**What's inside:**
- Feature list and benefits
- How it works (high-level)
- Setup overview
- Usage instructions
- Troubleshooting guide
- Customization options
- Cursor Cloud Agent integration

**Best for:** Understanding capabilities, general reference, troubleshooting

---

### Setup Instructions

**[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - 20 minutes (first time)  
Step-by-step guide to configure Slack, Confluence, and run the summarizer.

**What's inside:**
- Creating Slack bot with screenshots-level detail
- Generating Confluence API token
- Setting environment variables (3 methods)
- Installing dependencies
- Running the summarizer
- Verification steps
- Common issues and solutions
- Security best practices

**Best for:** First-time setup, detailed configuration, new team members

---

### Example Output

**[EXAMPLE_OUTPUT.md](./EXAMPLE_OUTPUT.md)** - 5 minutes  
Realistic example of what the Confluence summary looks like.

**What's inside:**
- Complete example summary from a realistic incident
- 5 team members with different roles
- All action categories demonstrated
- Link extraction examples
- Benefits and use cases
- Customization notes

**Best for:** Understanding output format, decision makers, preview before running

---

### Workflow & Architecture

**[WORKFLOW.md](./WORKFLOW.md)** - 15 minutes  
Deep dive into how the tool works, with process diagrams and technical details.

**What's inside:**
- Complete workflow diagram
- Phase-by-phase process flow
- Data flow examples (JSON → HTML)
- Error handling decision tree
- Performance characteristics
- Integration points
- Security considerations
- Future enhancements

**Best for:** Technical leads, architects, understanding internals, debugging

---

## 🎯 Choose Your Path

### I want to...

**...get started quickly**  
→ Read [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)  
→ Run `python3 test_config.py`  
→ Run `./run_summarizer.sh`

**...understand what this tool does**  
→ Read [INCIDENT_SUMMARIZER_README.md](./INCIDENT_SUMMARIZER_README.md)  
→ Check [EXAMPLE_OUTPUT.md](./EXAMPLE_OUTPUT.md)

**...set it up for the first time**  
→ Read [SETUP_GUIDE.md](./SETUP_GUIDE.md)  
→ Follow step-by-step instructions  
→ Use `test_config.py` to validate

**...see what the output looks like**  
→ Read [EXAMPLE_OUTPUT.md](./EXAMPLE_OUTPUT.md)

**...understand how it works**  
→ Read [WORKFLOW.md](./WORKFLOW.md)  
→ Review the code: `incident_channel_summarizer.py`

**...troubleshoot an error**  
→ Check [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) error table  
→ Review [SETUP_GUIDE.md](./SETUP_GUIDE.md) troubleshooting section  
→ Run `python3 test_config.py`

**...customize the output**  
→ Read [INCIDENT_SUMMARIZER_README.md](./INCIDENT_SUMMARIZER_README.md) customization section  
→ Check [WORKFLOW.md](./WORKFLOW.md) for data flow details

---

## 📖 Reading Order by Role

### For Engineers (First-Time Users)
1. [INCIDENT_SUMMARIZER_README.md](./INCIDENT_SUMMARIZER_README.md) - Understand features
2. [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Complete setup
3. [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Bookmark for later

### For Managers/Decision Makers
1. [EXAMPLE_OUTPUT.md](./EXAMPLE_OUTPUT.md) - See the value
2. [INCIDENT_SUMMARIZER_README.md](./INCIDENT_SUMMARIZER_README.md) - Understand capabilities
3. [WORKFLOW.md](./WORKFLOW.md) - Review process integration

### For DevOps/SRE
1. [WORKFLOW.md](./WORKFLOW.md) - Understand the system
2. [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Configuration details
3. [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Operational reference

### For Security Engineers
1. [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Security best practices
2. [WORKFLOW.md](./WORKFLOW.md) - Security considerations section
3. [INCIDENT_SUMMARIZER_README.md](./INCIDENT_SUMMARIZER_README.md) - OAuth scopes

### For New Team Members
1. [EXAMPLE_OUTPUT.md](./EXAMPLE_OUTPUT.md) - See what it produces
2. [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Set it up yourself
3. [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Keep handy

---

## 🔍 Quick Find

| I need to know... | Check this file | Section |
|------------------|-----------------|---------|
| How to run it | QUICK_REFERENCE.md | Quick Start Commands |
| Required environment variables | QUICK_REFERENCE.md | Environment Variables |
| How to create Slack bot | SETUP_GUIDE.md | Step 1: Create Slack Bot |
| How to get Confluence token | SETUP_GUIDE.md | Step 2: Get Confluence API Token |
| What the output looks like | EXAMPLE_OUTPUT.md | Confluence Page Output |
| Error message meaning | QUICK_REFERENCE.md | Common Error Solutions |
| Performance expectations | WORKFLOW.md | Performance Characteristics |
| Security considerations | WORKFLOW.md | Security Considerations |
| How to customize output | INCIDENT_SUMMARIZER_README.md | Customization |
| OAuth scopes needed | SETUP_GUIDE.md | Configure Bot Permissions |
| How pagination works | WORKFLOW.md | Detailed Process Flow |
| What gets categorized | QUICK_REFERENCE.md | Output Categories |
| Integration points | WORKFLOW.md | Integration Points |
| Future features | WORKFLOW.md | Future Enhancements |

---

## 📊 Documentation Stats

| File | Lines | Reading Time | Target Audience |
|------|-------|--------------|-----------------|
| QUICK_REFERENCE.md | ~200 | 2 min | Repeat users |
| INCIDENT_SUMMARIZER_README.md | ~170 | 10 min | All users |
| SETUP_GUIDE.md | ~350 | 20 min | New users |
| EXAMPLE_OUTPUT.md | ~250 | 5 min | Decision makers |
| WORKFLOW.md | ~500 | 15 min | Technical leads |
| **TOTAL** | **~1,470** | **52 min** | **Complete coverage** |

---

## 🔗 External Resources

### Slack API Documentation
- [Conversations API](https://api.slack.com/methods/conversations.history)
- [Users API](https://api.slack.com/methods/users.info)
- [OAuth Scopes](https://api.slack.com/scopes)
- [Creating Apps](https://api.slack.com/apps)

### Confluence API Documentation
- [REST API Examples](https://developer.atlassian.com/cloud/confluence/rest-api-examples)
- [API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Update Page](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-content/#api-wiki-rest-api-content-id-put)

### Python Libraries
- [slack-sdk](https://slack.dev/python-slack-sdk/)
- [atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api)

### Cursor Cloud Agents
- [Secrets Management](https://cursor.com/settings)
- [Cloud Agents Documentation](https://cursor.com/docs)

---

## 💡 Tips for Reading

1. **Start with your role** - Use the "Reading Order by Role" section above
2. **Use the Quick Find** - Jump directly to what you need
3. **Follow examples** - All docs include practical examples
4. **Test as you go** - Use `test_config.py` to validate each step
5. **Bookmark QUICK_REFERENCE** - You'll use it frequently

---

## 🤝 Contributing to Documentation

If you find errors or want to improve the documentation:

1. Check which file needs updating (use Quick Find table)
2. Make your changes with clear examples
3. Update this index if adding new sections
4. Test any code examples before committing
5. Submit a PR with description of changes

---

## 📝 Documentation Principles

Our documentation follows these principles:

- **Layered**: From quick reference to deep dives
- **Example-driven**: Every feature has examples
- **Role-specific**: Tailored to different users
- **Searchable**: Tables and indexes for quick lookup
- **Tested**: All commands and code are verified
- **Visual**: Diagrams and tables where helpful
- **Progressive**: Start simple, add complexity gradually

---

**Last Updated**: 2026-04-07  
**Documentation Version**: 1.0  
**Maintained by**: nesto.ca Engineering Team

For questions about this documentation, check the relevant file's support section or review the code comments in `incident_channel_summarizer.py`.
