# Terraform and GitHub Actions Integration

This document explains how the Terraform infrastructure pipeline integrates with GitHub Actions for automated deployment.

## Workflow Files

### `.github/workflows/terraform-deploy.yml`
- **Purpose**: Manages infrastructure deployment using Terraform
- **Triggers**: 
  - Push to `main` branch with changes in `terraform/` directory
  - Pull requests affecting `terraform/` directory
  - Manual trigger with optional destroy capability
- **Approval**: Requires manual approval for production deployments

### `.github/workflows/azure-webapp-deploy.yml`
- **Purpose**: Deploys application code to the provisioned infrastructure
- **Triggers**: 
  - Push to `main` branch (excluding `terraform/` changes)
  - Manual trigger
- **Authentication**: Supports both Service Principal and Publish Profile methods

## Deployment Flow

```
Code Push → Infrastructure Changes? 
    ├─ Yes → Terraform Workflow → Plan → Manual Approval → Apply → Infrastructure Ready
    └─ No  → App Deployment → Build & Test → Manual Approval → Deploy → Application Available
```

## Environment Protection

Both workflows use the `production` environment which can be configured in GitHub repository settings to require:
- Manual approval from designated reviewers
- Wait timers
- Branch protection rules
- Environment-specific secrets

## Best Practices

1. **Separate Concerns**: Infrastructure changes trigger only the Terraform workflow
2. **Manual Approval**: All production deployments require human approval
3. **State Management**: Terraform state is managed automatically by GitHub Actions
4. **Security**: Secrets are scoped to environments and workflows
5. **Rollback**: Infrastructure can be safely rolled back using the destroy option

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify GitHub Secrets are correctly configured
   - Ensure Service Principal has proper permissions
   - Check Azure subscription is active

2. **Resource Naming Conflicts**
   - App names must be globally unique
   - Consider using environment prefixes
   - Include random suffixes for dev environments

3. **Permission Errors**
   - Service Principal needs Contributor role
   - Resource Group permissions may be required
   - Check subscription-level access

### Debugging Steps

1. Review workflow logs in GitHub Actions
2. Check Azure Activity Log for resource operations
3. Validate Terraform plan before apply
4. Verify secrets are properly masked in logs