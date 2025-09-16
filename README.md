# KarelAgent Data & Analytics Platform

## Overview
This project is an advanced data and analytics platform powered by LangChain agents. The architecture includes:
- **CEO Agent**: Central decision-maker, approves all critical actions.
- **Specialist Agents**: Data Ingestion, Data Cleaning, Analytics, Visualization, Reporting.
- **Agent Communication**: Agents communicate and collaborate, but require CEO approval for final decisions.
- **REST API Endpoints**: For agent communication and decision approval.

## Tech Stack
- Python
- LangChain
- FastAPI

## Getting Started
1. Install dependencies (see `requirements.txt`).
2. Run the platform using FastAPI.
3. Interact with agents via API endpoints.

## GitHub Pages
- Visit our GitHub Pages site at: [KarelAgent GitHub Pages](https://karelgo.github.io/KarelAgent)

## Azure Web App Deployment

### CI/CD Pipeline
This project includes a GitHub Actions workflow that automatically deploys the Streamlit app to Azure Web App Service on every push to the main branch.

## Infrastructure as Code (Terraform)

This project uses Terraform to manage Azure infrastructure. You can either use the automated Terraform approach (recommended) or manually create resources.

### Option 1: Automated Infrastructure with Terraform (Recommended)

The repository includes Terraform configurations to automatically provision all required Azure resources.

#### Required GitHub Secrets for Terraform

Configure the following secrets in your GitHub repository (Settings → Secrets and variables → Actions):

1. **AZURE_CLIENT_ID**: Application (client) ID of your Azure service principal
2. **AZURE_CLIENT_SECRET**: Client secret of your Azure service principal  
3. **AZURE_SUBSCRIPTION_ID**: Your Azure subscription ID
4. **AZURE_TENANT_ID**: Your Azure tenant ID
5. **AZURE_WEBAPP_NAME**: Desired name for your web app (must be globally unique)

#### Setting up Azure Service Principal

You can create the required Azure Service Principal using either the automated GitHub Actions workflow (recommended) or manually using the Azure CLI.

> **Note**: The service principal will be created with the pre-configured Azure subscription ID: `4910a5a6-aec6-405d-9294-c7f2845512a4`

##### Option A: Automated Service Principal Creation (Recommended)

1. **Prerequisites:**
   - You must have existing Azure credentials configured as GitHub Secrets (if you don't have them yet, use Option B first)
   - You need write access to the repository to run workflows

2. **Trigger the Workflow:**
   - Go to your GitHub repository
   - Navigate to **Actions** → **Create Azure Service Principal**
   - Click **Run workflow**
   - Optionally customize the service principal name
   - Choose whether to automatically update GitHub secrets (recommended)

2. **Manual Approval:**
   - The workflow requires manual approval for security
   - Review the workflow details and approve the run

3. **Automatic Configuration:**
   - The workflow will create the service principal with the pre-configured subscription ID
   - GitHub secrets will be automatically updated (if enabled)
   - All credentials will be securely stored

##### Option B: Manual Service Principal Creation

1. **Install Azure CLI** (if not already installed):
   ```bash
   # On macOS
   brew install azure-cli
   
   # On Ubuntu/Debian
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Login to Azure:**
   ```bash
   az login
   ```

3. **Run the provided script:**
   ```bash
   # Execute the service principal creation script
   ./scripts/create-service-principal.sh
   ```

   Or create manually:
   ```bash
   # Create service principal with the configured subscription ID
   az ad sp create-for-rbac --name "karelAgent-github-actions" \
     --role="Contributor" \
     --scopes="/subscriptions/4910a5a6-aec6-405d-9294-c7f2845512a4" \
     --query '{appId:appId, password:password, tenant:tenant}' \
     --output json
   ```

4. **Configure GitHub Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `AZURE_CLIENT_ID` → Application (client) ID from the output
     - `AZURE_CLIENT_SECRET` → Password from the output
     - `AZURE_SUBSCRIPTION_ID` → `4910a5a6-aec6-405d-9294-c7f2845512a4`
     - `AZURE_TENANT_ID` → Tenant ID from the output

#### Using Terraform

1. **Configure Variables:** Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and update the values.

2. **Deploy Infrastructure:** Push changes to the `terraform/` directory or manually trigger the "Deploy Infrastructure with Terraform" workflow.

3. **Manual Approval:** The workflow requires manual approval before applying changes to protect against accidental modifications.

4. **Access Your Application:** After successful deployment, your app will be available at the URL shown in the workflow output.

#### Troubleshooting Service Principal Setup

**Common Issues:**

1. **Workflow fails with authentication error:**
   - Ensure you have existing Azure credentials as GitHub Secrets
   - For first-time setup, use Option B (manual creation) to bootstrap the initial credentials

2. **Permission denied errors:**
   - Verify you have sufficient permissions in the Azure subscription
   - Check that you're logged into the correct Azure account (`az account show`)

3. **Service principal already exists:**
   - The workflow will automatically reset credentials for existing service principals
   - You can also manually delete the existing SP in Azure Portal and re-run the workflow

4. **Secrets update fails:**
   - Ensure the GitHub token has proper permissions
   - Try running the workflow with "update_secrets" set to false and manually configure secrets

**For additional help:** Check the GitHub Actions workflow logs for detailed error messages and troubleshooting information.

### Option 2: Manual Azure Resource Setup (Legacy)

#### Setting up Azure Credentials

To enable automatic deployment with manually created resources, you need to configure the following GitHub Secrets:

1. **AZURE_WEBAPP_NAME**: The name of your Azure Web App
2. **AZURE_WEBAPP_PUBLISH_PROFILE**: The publish profile XML content for your Azure Web App

#### Step-by-step setup:

1. **Create an Azure Web App:**
   - Go to the Azure Portal (https://portal.azure.com)
   - Create a new Web App with Python runtime
   - Choose your subscription and resource group
   - Note down the app name for `AZURE_WEBAPP_NAME`

2. **Get the Publish Profile:**
   - In the Azure Portal, go to your Web App
   - Click "Get publish profile" to download the `.publishsettings` file
   - Open the file and copy its entire contents

3. **Configure GitHub Secrets:**
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Add these repository secrets:
     - `AZURE_WEBAPP_NAME`: Your Azure Web App name
     - `AZURE_WEBAPP_PUBLISH_PROFILE`: Paste the entire content of the publish profile XML

4. **Deploy:**
   - Push changes to the main branch
   - The GitHub Action will automatically build and deploy your Streamlit app
   - Your app will be available at `https://your-app-name.azurewebsites.net`

## Deployment Workflows

### Infrastructure Deployment (Terraform)
- **Workflow:** `.github/workflows/terraform-deploy.yml`
- **Triggers:** Changes to `terraform/` directory, manual trigger
- **Features:** 
  - Automated Terraform plan and apply
  - Manual approval required for production changes
  - Infrastructure as Code with state management
  - Support for destroy operations

### Application Deployment
- **Workflow:** `.github/workflows/azure-webapp-deploy.yml`
- **Triggers:** Changes to application code (excluding `terraform/`)
- **Features:**
  - Supports both Service Principal and Publish Profile authentication
  - Automatic detection of authentication method
  - Manual approval required for production deployments

### Local Development
1. Install dependencies: `pip install -r agentsetup/requirements.txt`
2. Run the Streamlit app: `cd agentsetup && streamlit run streamlit_app.py`
3. Run the FastAPI backend: `cd agentsetup && uvicorn main:app --reload`

## Next Steps
- Implement agent classes and orchestration logic.
- Add inter-agent communication and CEO approval flow.
- Expand platform features as needed.