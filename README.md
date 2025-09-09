# KarelAgent Data & Analytics Platform

## Overview
This project is an advanced data and analytics platform powered by LangChain agents. The architecture includes:
- **CEO Agent**: Central decision-maker, approves all critical actions.
- **Specialist Agents**: Data Ingestion, Data Cleaning, Analytics, Visualization, Reporting.
- **Agent Communication**: Agents communicate and collaborate, but require CEO approval for final decisions.
- **REST API Endpoints**: For agent communication and decision approval.
- **Frontend Application**: A responsive web interface showcasing the platform capabilities.

## Tech Stack
### Backend
- Python
- LangChain
- FastAPI

### Frontend
- HTML5
- CSS3 (with responsive design)
- Vanilla JavaScript
- Vercel-ready static deployment

## Project Structure
```
KarelAgent/
├── agentsetup/          # Backend Python code
│   ├── main.py          # FastAPI application
│   ├── agents.py        # Agent implementations
│   ├── requirements.txt # Python dependencies
│   └── ...
├── frontend/            # Frontend application
│   ├── index.html       # Home page
│   ├── about.html       # About page
│   ├── styles.css       # Responsive styles
│   └── script.js        # JavaScript functionality
├── vercel.json          # Vercel deployment configuration
└── README.md           # This file
```

## Frontend Application Features
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Navigation**: Clean navigation bar with Home and About links
- **Home Page**: Welcoming message and platform overview
- **About Page**: Detailed information about the platform architecture
- **Modern UI**: Professional styling with smooth animations

## Deployment on Vercel

### Quick Deploy
1. **Fork or Clone** this repository to your GitHub account
2. **Connect to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign up/login with your GitHub account
   - Click "New Project"
   - Import your KarelAgent repository
3. **Deploy**:
   - Vercel will automatically detect the configuration
   - Click "Deploy"
   - Your application will be live in minutes!

### Manual Deployment
1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project root**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Confirm project name
   - Choose deployment settings
   - Get your live URL

### Configuration
The `vercel.json` file is pre-configured to:
- Serve the frontend application as static files
- Route requests correctly to HTML pages
- Set up proper caching headers
- Include security headers

### Custom Domain (Optional)
After deployment, you can add a custom domain:
1. Go to your project dashboard on Vercel
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Local Development

### Backend Setup
1. Navigate to the agentsetup directory:
   ```bash
   cd agentsetup
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Development
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the files locally (using Python):
   ```bash
   python -m http.server 8000
   ```

3. Open your browser to `http://localhost:8000`

### Preview Frontend Locally
You can also use any static file server:
```bash
# Using Node.js serve
npx serve frontend

# Using Python
cd frontend && python -m http.server 3000
```

## Environment URLs
- **Production**: Your Vercel deployment URL (e.g., `https://your-project.vercel.app`)
- **Local Frontend**: `http://localhost:8000` (or your chosen port)
- **Local Backend**: `http://localhost:8000` (FastAPI with uvicorn)

## Next Steps
- Implement agent classes and orchestration logic
- Add inter-agent communication and CEO approval flow
- Connect frontend to backend APIs
- Expand platform features as needed
- Add authentication and user management
