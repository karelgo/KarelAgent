#!/bin/bash

# Azure Service Principal Creation Script
# This script creates a service principal for GitHub Actions with Contributor role

set -e

# Configuration
SUBSCRIPTION_ID="4910a5a6-aec6-405d-9294-c7f2845512a4"
SP_NAME="karelAgent-github-actions"
ROLE="Contributor"

echo "🔐 Creating Azure Service Principal for GitHub Actions..."
echo "📋 Configuration:"
echo "  - Subscription ID: $SUBSCRIPTION_ID"
echo "  - Service Principal Name: $SP_NAME"
echo "  - Role: $ROLE"
echo

# Check if Azure CLI is logged in
echo "🔍 Checking Azure CLI authentication..."
if ! az account show &>/dev/null; then
    echo "❌ Error: Not logged in to Azure CLI"
    echo "Please run 'az login' first to authenticate"
    exit 1
fi

# Set the subscription
echo "🎯 Setting Azure subscription..."
az account set --subscription "$SUBSCRIPTION_ID"

# Verify subscription access
CURRENT_SUB=$(az account show --query id -o tsv)
if [ "$CURRENT_SUB" != "$SUBSCRIPTION_ID" ]; then
    echo "❌ Error: Cannot access subscription $SUBSCRIPTION_ID"
    echo "Current subscription: $CURRENT_SUB"
    exit 1
fi

echo "✅ Successfully set subscription to: $SUBSCRIPTION_ID"

# Create service principal
echo "👤 Creating service principal..."
if ! SP_OUTPUT=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role "$ROLE" \
    --scopes "/subscriptions/$SUBSCRIPTION_ID" \
    --query '{appId:appId, displayName:displayName, password:password, tenant:tenant}' \
    --output json); then
    echo "❌ Error: Failed to create service principal"
    exit 1
fi

echo "✅ Service principal created successfully!"
echo

# Extract credentials
APP_ID=$(echo "$SP_OUTPUT" | jq -r '.appId')
PASSWORD=$(echo "$SP_OUTPUT" | jq -r '.password')
TENANT_ID=$(echo "$SP_OUTPUT" | jq -r '.tenant')

# Display results
echo "🔑 Service Principal Details:"
echo "=============================================="
echo "Service Principal Name: $SP_NAME"
echo "Application ID (Client ID): $APP_ID"
echo "Tenant ID: $TENANT_ID"
echo "Subscription ID: $SUBSCRIPTION_ID"
echo "Role: $ROLE"
echo "=============================================="
echo

echo "📝 GitHub Secrets to Configure:"
echo "=============================================="
echo "AZURE_CLIENT_ID: $APP_ID"
echo "AZURE_CLIENT_SECRET: [MASKED - see secure output below]"
echo "AZURE_SUBSCRIPTION_ID: $SUBSCRIPTION_ID"
echo "AZURE_TENANT_ID: $TENANT_ID"
echo "=============================================="
echo

echo "🔒 SECURE OUTPUT (Client Secret):"
echo "=============================================="
echo "AZURE_CLIENT_SECRET: $PASSWORD"
echo "=============================================="
echo

echo "⚠️  IMPORTANT SECURITY NOTES:"
echo "1. Save the client secret above immediately - it cannot be retrieved later"
echo "2. Add these values as GitHub Secrets in your repository settings"
echo "3. Never commit these credentials to source code"
echo "4. The client secret is only shown once for security reasons"
echo

echo "📚 Next Steps:"
echo "1. Go to your GitHub repository settings"
echo "2. Navigate to Settings → Secrets and variables → Actions"
echo "3. Add each of the GitHub Secrets listed above"
echo "4. Use the service principal credentials in your GitHub Actions workflows"
echo

echo "✨ Service principal creation completed successfully!"