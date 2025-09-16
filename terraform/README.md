# Terraform Infrastructure

This directory contains Terraform configurations to provision Azure infrastructure for the KarelAgent application.

## Files

- **`main.tf`**: Main Terraform configuration defining Azure resources
- **`variables.tf`**: Variable definitions and validation rules
- **`outputs.tf`**: Output values from the Terraform deployment
- **`terraform.tfvars.example`**: Example configuration file (copy to `terraform.tfvars`)

## Resources Created

The Terraform configuration creates the following Azure resources:

1. **Resource Group**: Container for all resources
2. **App Service Plan**: Defines the compute resources for the web app
3. **Linux Web App**: The main application hosting service
4. **Application Insights**: Monitoring and analytics service
5. **Staging Slot** (optional): For blue-green deployments

## Configuration

1. Copy `terraform.tfvars.example` to `terraform.tfvars`
2. Update the `app_name` value (must be globally unique)
3. Adjust other settings as needed

## Usage

### Via GitHub Actions (Recommended)

The infrastructure is automatically managed through the GitHub Actions workflow:
- Push changes to the `terraform/` directory
- The workflow will plan and apply changes with manual approval

### Manual Deployment

If you need to run Terraform manually:

```bash
# Initialize Terraform
terraform init

# Plan changes
terraform plan -var="app_name=your-unique-app-name"

# Apply changes
terraform apply -var="app_name=your-unique-app-name"
```

## Important Notes

- The `app_name` must be globally unique across all Azure Web Apps
- The configuration includes Application Insights for monitoring
- Staging slots are disabled by default (set `enable_staging_slot = true` to enable)
- Always review the plan before applying changes in production