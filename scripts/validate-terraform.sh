#!/bin/bash

# Terraform Infrastructure Validation Script
# This script validates the Terraform configuration without requiring Azure credentials

set -e

TERRAFORM_DIR="./terraform"

echo "🔍 Validating Terraform Infrastructure Configuration..."
echo

# Check if terraform directory exists
if [ ! -d "$TERRAFORM_DIR" ]; then
    echo "❌ Error: terraform directory not found"
    exit 1
fi

cd "$TERRAFORM_DIR"

# Check required files exist
echo "📁 Checking required files..."
REQUIRED_FILES=("main.tf" "variables.tf" "outputs.tf" "terraform.tfvars.example")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        exit 1
    fi
done
echo

# Validate Terraform formatting
echo "🎨 Checking Terraform formatting..."
if terraform fmt -check -diff > /dev/null 2>&1; then
    echo "  ✅ All files properly formatted"
else
    echo "  ⚠️  Files need formatting. Run 'terraform fmt' to fix."
fi
echo

# Validate Terraform configuration syntax
echo "🔧 Validating Terraform configuration..."
if terraform validate > /dev/null 2>&1; then
    echo "  ✅ Configuration is valid"
else
    echo "  ❌ Configuration validation failed"
    terraform validate
    exit 1
fi
echo

echo "✨ Terraform configuration validation completed successfully!"
echo
echo "📋 Summary:"
echo "  - All required files present"
echo "  - Configuration syntax is valid" 
echo "  - Ready for deployment with proper Azure credentials"
echo
echo "🚀 Next steps:"
echo "  1. Configure GitHub Secrets for Azure authentication"
echo "  2. Set AZURE_WEBAPP_NAME to a globally unique value"
echo "  3. Push changes to trigger the Terraform workflow"

exit 0