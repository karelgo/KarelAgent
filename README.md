# KarelAgent Data & Analytics Platform

## Overview
This project is an advanced data and analytics platform powered by LangChain agents. The platform includes both a backend API and a modern web frontend.

### Platform Components:
- **Frontend Web Application**: Modern, responsive Flask-based web interface
- **Backend API**: FastAPI-powered agent orchestration system
- **CEO Agent**: Central decision-maker, approves all critical actions
- **Specialist Agents**: Data Ingestion, Data Cleaning, Analytics, Visualization, Reporting
- **Agent Communication**: Agents communicate and collaborate, but require CEO approval for final decisions

## Tech Stack
- **Frontend**: Python (Flask), HTML5, CSS3, Responsive Design
- **Backend**: Python, LangChain, FastAPI
- **Deployment**: Vercel-ready configuration

## Frontend Web Application

The main web application provides a user-friendly interface with:
- **Home Page**: Welcome message and platform overview
- **About Page**: Detailed project information and technical architecture
- **Responsive Design**: Optimized for desktop and mobile devices
- **Modern UI**: Clean, professional interface with intuitive navigation

### Running the Frontend Locally

1. Install frontend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask development server:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`

## Vercel Deployment

The application is configured for seamless deployment on Vercel:

### Prerequisites
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Vercel CLI (optional, for command-line deployment)

### Deployment Methods

#### Method 1: GitHub Integration (Recommended)
1. Push your code to a GitHub repository
2. Connect your GitHub account to Vercel
3. Import the repository in your Vercel dashboard
4. Vercel will automatically detect the Python application and deploy it
5. The `vercel.json` configuration file ensures proper routing

#### Method 2: Vercel CLI
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from the project root:
   ```bash
   vercel
   ```

4. Follow the prompts to configure your deployment

#### Method 3: Drag & Drop
1. Zip your project files (excluding `.git` and `__pycache__` folders)
2. Visit [vercel.com/new](https://vercel.com/new)
3. Drag and drop your zip file
4. Vercel will automatically deploy your application

### Environment Configuration

The `vercel.json` file includes:
- Python runtime configuration
- Route handling for the Flask application
- Environment variables setup

### Custom Domain (Optional)
After deployment, you can configure a custom domain in your Vercel dashboard under the "Domains" section.

## Backend API (Agent System)

The backend agent system is located in the `agentsetup/` directory.

### Running the Backend Locally

1. Navigate to the agentsetup directory:
   ```bash
   cd agentsetup
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation at `http://127.0.0.1:8000/docs`

### API Endpoints
- **POST /ingest**: Data ingestion operations
- **POST /clean**: Data cleaning operations  
- **POST /analyze**: Data analysis operations
- **POST /visualize**: Data visualization operations
- **POST /report**: Report generation operations

## Project Structure

```
KarelAgent/
├── app.py                 # Flask web application
├── requirements.txt       # Frontend dependencies
├── vercel.json           # Vercel deployment configuration
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── home.html        # Home page template
│   └── about.html       # About page template
├── agentsetup/           # Backend agent system
│   ├── main.py          # FastAPI application
│   ├── agents.py        # Agent implementations
│   ├── base_agent.py    # Base agent class
│   ├── ceo_agent.py     # CEO approval system
│   ├── requirements.txt # Backend dependencies
│   └── streamlit_app.py # Alternative Streamlit interface
└── README.md            # This file
```

## Development Workflow

1. **Frontend Development**: Edit templates and Flask routes in the root directory
2. **Backend Development**: Modify agent logic in the `agentsetup/` directory
3. **Testing**: Run both frontend and backend locally for full-stack testing
4. **Deployment**: Push to GitHub for automatic Vercel deployment

## Contributing

KarelAgent is an open-source project under the MIT License. We welcome contributions, feedback, and collaboration from the developer community.

## Next Steps
- Implement agent classes and orchestration logic
- Add inter-agent communication and CEO approval flow
- Integrate frontend with backend API
- Expand platform features as needed
