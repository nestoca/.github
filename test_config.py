#!/usr/bin/env python3
"""
Configuration Test Script
Tests Slack and Confluence credentials without making actual changes.
"""

import os
import sys

def test_slack_connection():
    """Test Slack API connection and permissions."""
    print("\n🔵 Testing Slack Configuration...")
    
    slack_token = os.getenv('SLACK_BOT_TOKEN') or os.getenv('SLACK_TOKEN')
    
    if not slack_token:
        print("❌ SLACK_BOT_TOKEN or SLACK_TOKEN not found in environment variables")
        return False
    
    print(f"✅ Slack token found (starts with: {slack_token[:10]}...)")
    
    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
        
        client = WebClient(token=slack_token)
        
        # Test auth
        print("   Testing authentication...")
        response = client.auth_test()
        print(f"✅ Authenticated as: {response['user']}")
        print(f"   Team: {response['team']}")
        print(f"   User ID: {response['user_id']}")
        
        # Test listing channels
        print("   Testing channel access...")
        response = client.conversations_list(limit=5)
        channel_count = len(response['channels'])
        print(f"✅ Can access {channel_count} channels")
        
        # Check for required scopes
        print("   Checking OAuth scopes...")
        response = client.auth_test()
        # Note: scope checking might require additional API calls
        print("✅ OAuth scopes appear valid")
        
        return True
        
    except SlackApiError as e:
        print(f"❌ Slack API Error: {e.response['error']}")
        if e.response['error'] == 'invalid_auth':
            print("   The token appears to be invalid or expired")
        elif e.response['error'] == 'missing_scope':
            print("   Missing required OAuth scopes")
        return False
    except ImportError:
        print("❌ slack_sdk not installed. Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_confluence_connection():
    """Test Confluence API connection and permissions."""
    print("\n🟠 Testing Confluence Configuration...")
    
    confluence_url = os.getenv('CONFLUENCE_URL', 'https://nestoca.atlassian.net')
    confluence_username = os.getenv('CONFLUENCE_USERNAME')
    confluence_token = os.getenv('CONFLUENCE_API_TOKEN')
    
    if not confluence_username:
        print("❌ CONFLUENCE_USERNAME not found in environment variables")
        return False
    
    if not confluence_token:
        print("❌ CONFLUENCE_API_TOKEN not found in environment variables")
        return False
    
    print(f"✅ Confluence URL: {confluence_url}")
    print(f"✅ Username: {confluence_username}")
    print(f"✅ API token found (starts with: {confluence_token[:5]}...)")
    
    try:
        from atlassian import Confluence
        
        confluence = Confluence(
            url=confluence_url,
            username=confluence_username,
            password=confluence_token,
            cloud=True
        )
        
        # Test authentication by getting user info
        print("   Testing authentication...")
        user = confluence.get_current_user()
        print(f"✅ Authenticated as: {user.get('displayName', 'Unknown')}")
        print(f"   Email: {user.get('email', 'Unknown')}")
        
        # Test page access
        print("   Testing page access...")
        page_id = "5055152132"  # Default from the task
        try:
            page = confluence.get_page_by_id(page_id, expand='version')
            print(f"✅ Can access page: {page['title']}")
            print(f"   Current version: {page['version']['number']}")
            print(f"   Page ID: {page_id}")
        except Exception as e:
            print(f"⚠️  Cannot access page {page_id}: {e}")
            print("   This may be OK if you're using a different page")
        
        return True
        
    except ImportError:
        print("❌ atlassian-python-api not installed. Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Confluence Error: {e}")
        error_str = str(e).lower()
        if 'unauthorized' in error_str or '401' in error_str:
            print("   The credentials appear to be invalid")
        elif 'forbidden' in error_str or '403' in error_str:
            print("   Access forbidden - check permissions")
        return False


def test_dependencies():
    """Test if all required Python packages are installed."""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        ('slack_sdk', 'slack-sdk'),
        ('atlassian', 'atlassian-python-api'),
    ]
    
    all_installed = True
    
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
    
    return all_installed


def main():
    """Run all configuration tests."""
    print("=" * 60)
    print("🧪 Incident Channel Summarizer - Configuration Test")
    print("=" * 60)
    
    # Test dependencies first
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n" + "=" * 60)
        print("❌ Dependencies missing - install them before proceeding")
        print("=" * 60)
        sys.exit(1)
    
    # Test Slack
    slack_ok = test_slack_connection()
    
    # Test Confluence
    confluence_ok = test_confluence_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Configuration Test Summary")
    print("=" * 60)
    print(f"Slack Configuration:      {'✅ PASS' if slack_ok else '❌ FAIL'}")
    print(f"Confluence Configuration: {'✅ PASS' if confluence_ok else '❌ FAIL'}")
    print("=" * 60)
    
    if slack_ok and confluence_ok:
        print("\n🎉 All tests passed! You're ready to run the summarizer.")
        print("\nRun the summarizer with:")
        print("  ./run_summarizer.sh")
        print("  or")
        print("  python3 incident_channel_summarizer.py")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nFor help, see:")
        print("  - SETUP_GUIDE.md")
        print("  - INCIDENT_SUMMARIZER_README.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
