# KarelAgent Data & Analytics Platform

## Overview
This project is an advanced data and analytics platform powered by LangChain agents. The architecture includes:
- **CEO Agent**: Central decision-maker, approves all critical actions.
- **Specialist Agents**: Data Ingestion, Data Cleaning, Analytics, Visualization, Reporting.
- **Agent Communication**: Agents communicate and collaborate, but require CEO approval for final decisions.
- **REST API Endpoints**: For agent communication and decision approval.
- **Streamlit Frontend**: Web interface for interacting with the agents.

## Tech Stack
- Python
- LangChain
- FastAPI (Backend API)
- Streamlit (Frontend Web App)

## Getting Started

### Local Development
1. Install dependencies:
   ```bash
   cd agentsetup
   pip install -r requirements.txt
   ```

2. Run the FastAPI backend:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. Run the Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

### Azure Web App Deployment

This repository includes a CI/CD pipeline that automatically deploys the Streamlit app to Azure Web App Service when code is pushed to the main branch.

#### Prerequisites
1. An Azure Web App Service instance configured for Python
2. GitHub repository secrets configured (see below)

#### Required GitHub Secrets

To enable automatic deployment to Azure Web App Service, you need to configure the following secrets in your GitHub repository:

1. **AZURE_WEBAPP_NAME**: The name of your Azure Web App Service
   - Example: `karelAgent-webapp`

2. **AZURE_WEBAPP_PUBLISH_PROFILE**: The publish profile XML content from your Azure Web App
   - How to get this:
     1. Go to your Azure Web App in the Azure Portal
     2. Click on "Get publish profile" in the top menu
     3. Copy the entire contents of the downloaded `.PublishSettings` file
     4. Paste this as the value for the secret

#### Setting Up GitHub Secrets

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click on "Secrets and variables" → "Actions"
4. Click "New repository secret" and add each secret:
   - Name: `AZURE_WEBAPP_NAME`, Value: Your Azure Web App name
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`, Value: Your publish profile XML content

#### Azure Web App Configuration

Make sure your Azure Web App is configured with:
- **Runtime**: Python 3.11
- **Startup Command**: `python startup.py`
- **Port**: The app will automatically use the PORT environment variable provided by Azure

#### Environment Variables (Optional)

You can configure the following environment variables in your Azure Web App:
- `BACKEND_URL`: URL of the FastAPI backend (if running separately)

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/azure-deploy.yml`) automatically:

1. **Triggers on**: Every push to the main branch
2. **Build and Test**: 
   - Sets up Python environment
   - Installs dependencies
   - Runs import tests
   - Validates Streamlit app syntax
3. **Deploy**: 
   - Creates a deployment package
   - Deploys to Azure Web App Service using the publish profile

## GitHub Pages
- Visit our GitHub Pages site at: [KarelAgent GitHub Pages](https://karelgo.github.io/KarelAgent)

## Architecture Notes

The Streamlit app serves as a frontend that communicates with the FastAPI backend. In a production deployment, you may want to:
- Deploy the FastAPI backend as a separate Azure Web App or Container Instance
- Configure the `BACKEND_URL` environment variable to point to your backend service
- Set up proper authentication and security measures

## Next Steps
- Implement agent classes and orchestration logic.
- Add inter-agent communication and CEO approval flow.
- Expand platform features as needed.
- Add comprehensive testing suite.
- Implement proper logging and monitoring.