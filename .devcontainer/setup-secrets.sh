#!/bin/bash
# Load secrets from GitHub Codespace and set as environment variables
echo "Loading secrets from GitHub repository..."

GH_ACCOUNT=$(gh secret get GH_ACCOUNT --repo $GITHUB_REPOSITORY 2>/dev/null)
GH_APPKEY=$(gh secret get GH_APPKEY --repo $GITHUB_REPOSITORY 2>/dev/null)
GH_APPSECRET=$(gh secret get GH_APPSECRET --repo $GITHUB_REPOSITORY 2>/dev/null)

if [ -z "$GH_ACCOUNT" ] || [ -z "$GH_APPKEY" ] || [ -z "$GH_APPSECRET" ]; then
    echo "Warning: Some secrets not found. Please ensure GH_ACCOUNT, GH_APPKEY, GH_APPSECRET are set in repository secrets."
    echo "You can also manually create a .env file in samsung_auto_trader/ directory."
else
    # Write to .env file for python-dotenv
    echo "GH_ACCOUNT=$GH_ACCOUNT" > samsung_auto_trader/.env
    echo "GH_APPKEY=$GH_APPKEY" >> samsung_auto_trader/.env
    echo "GH_APPSECRET=$GH_APPSECRET" >> samsung_auto_trader/.env
    echo "Secrets loaded successfully."
fi