# GCP Gemini API Audit Scripts

This directory contains scripts to help audit and manage GCP projects with the Gemini API enabled.

## Quick Commands

If you prefer to run commands directly without the script, here are the key gcloud commands:

### List all projects with Gemini API enabled

```bash
# Get all project IDs
PROJECT_IDS=$(gcloud projects list --format="value(projectId)")

# Check each project for Gemini API
for project in $PROJECT_IDS; do
  if gcloud services list --enabled --project="$project" --format="value(config.name)" 2>/dev/null | grep -q "generativelanguage.googleapis.com"; then
    echo "Gemini API enabled in: $project"
  fi
done
```

### Check for unrestricted API keys in a specific project

```bash
PROJECT_ID="your-project-id"

# List all API keys (requires alpha component)
gcloud alpha services api-keys list --project="$PROJECT_ID" --format="json"

# To see detailed restrictions on a specific key
gcloud alpha services api-keys describe KEY_ID --project="$PROJECT_ID"
```

### Fix unrestricted API keys

```bash
# Option 1: Add API restrictions to an existing key
gcloud alpha services api-keys update KEY_ID \
  --project="$PROJECT_ID" \
  --api-target=service=generativelanguage.googleapis.com

# Option 2: Add HTTP referrer restrictions (for web apps)
gcloud alpha services api-keys update KEY_ID \
  --project="$PROJECT_ID" \
  --allowed-referrers="https://yourdomain.com/*"

# Option 3: Add IP address restrictions
gcloud alpha services api-keys update KEY_ID \
  --project="$PROJECT_ID" \
  --allowed-ips="203.0.113.0/24"
```

## Using the Audit Script

The `gcp-gemini-api-audit.sh` script automates the process of finding projects with the Gemini API enabled and identifying unrestricted API keys.

### Prerequisites

1. Install the gcloud CLI: https://cloud.google.com/sdk/docs/install
2. Authenticate: `gcloud auth login`
3. Install jq (for JSON parsing): 
   - macOS: `brew install jq`
   - Ubuntu/Debian: `sudo apt-get install jq`
   - Other: https://stedolan.github.io/jq/download/

### Usage

```bash
# Make the script executable
chmod +x scripts/gcp-gemini-api-audit.sh

# Run the audit
./scripts/gcp-gemini-api-audit.sh
```

### What the script does

1. ✅ Lists all GCP projects you have access to
2. ✅ Checks each project for the Gemini API (`generativelanguage.googleapis.com`)
3. ✅ For projects with Gemini API enabled, checks for unrestricted API keys
4. ✅ Provides a summary with projects requiring action
5. ✅ Suggests remediation commands

### Sample Output

```
=== GCP Gemini API & Unrestricted API Keys Audit ===

Fetching all accessible GCP projects...

Scanning projects for Gemini API (generativelanguage.googleapis.com)...

Checking project: my-project-1... [Gemini API ENABLED]
  └─ Checking for unrestricted API keys... [UNRESTRICTED KEYS FOUND]
Checking project: my-project-2... [Not enabled]

=== Summary ===
Total projects scanned: 2
Projects with Gemini API enabled: 1
Projects with unrestricted API keys: 1

=== Projects with Gemini API Enabled ===
my-project-1

=== ⚠️  PROJECTS REQUIRING ACTION (Unrestricted API Keys) ===
my-project-1

To fix unrestricted API keys, run:
gcloud alpha services api-keys list --project=PROJECT_ID
gcloud alpha services api-keys update KEY_ID --project=PROJECT_ID --api-target=service=SERVICE_NAME

Or visit: https://console.cloud.google.com/apis/credentials
```

## Additional Resources

- [GCP API Keys Best Practices](https://cloud.google.com/docs/authentication/api-keys)
- [Restricting API Keys](https://cloud.google.com/docs/authentication/api-keys#api-keys-restrictions)
- [Gemini API Documentation](https://ai.google.dev/docs)

## Troubleshooting

### "gcloud: command not found"
Install the gcloud CLI from https://cloud.google.com/sdk/docs/install

### "Permission denied" errors
Ensure you have the necessary IAM permissions:
- `resourcemanager.projects.get`
- `serviceusage.services.list`
- `apikeys.keys.list`

### "jq: command not found"
Install jq for JSON parsing or modify the script to use alternative JSON parsing methods.
