#!/bin/bash

# Azure Web App startup script for Streamlit
echo "Starting Streamlit application..."

# Set environment variables
export STREAMLIT_SERVER_PORT=${PORT:-8000}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Navigate to the application directory
cd /home/site/wwwroot

# Install dependencies if not already installed
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start Streamlit
streamlit run streamlit_app.py --server.port=$STREAMLIT_SERVER_PORT --server.address=$STREAMLIT_SERVER_ADDRESS --server.headless=$STREAMLIT_SERVER_HEADLESS