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

### Setting up Azure Credentials

To enable automatic deployment, you need to configure the following GitHub Secrets in your repository:

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

### Local Development
1. Install dependencies: `pip install -r agentsetup/requirements.txt`
2. Run the Streamlit app: `cd agentsetup && streamlit run streamlit_app.py`
3. Run the FastAPI backend: `cd agentsetup && uvicorn main:app --reload`

## Next Steps
- Implement agent classes and orchestration logic.
- Add inter-agent communication and CEO approval flow.
- Expand platform features as needed.