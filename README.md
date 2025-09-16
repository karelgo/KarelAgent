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

3. **Create a Service Principal:**
   ```bash
   # Replace 'your-subscription-id' with your actual subscription ID
   az ad sp create-for-rbac --name "terraform-github-actions" \
     --role="Contributor" \
     --scopes="/subscriptions/your-subscription-id" \
     --sdk-auth
   ```

4. **Copy the output JSON** and extract the following values for GitHub Secrets:
   - `clientId` → `AZURE_CLIENT_ID`
   - `clientSecret` → `AZURE_CLIENT_SECRET`
   - `subscriptionId` → `AZURE_SUBSCRIPTION_ID`
   - `tenantId` → `AZURE_TENANT_ID`

#### Using Terraform

1. **Configure Variables:** Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and update the values.

2. **Deploy Infrastructure:** Push changes to the `terraform/` directory or manually trigger the "Deploy Infrastructure with Terraform" workflow.

3. **Manual Approval:** The workflow requires manual approval before applying changes to protect against accidental modifications.

4. **Access Your Application:** After successful deployment, your app will be available at the URL shown in the workflow output.

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