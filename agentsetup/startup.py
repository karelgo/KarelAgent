import os
import subprocess
import sys

if __name__ == "__main__":
    # Get the port from environment variable
    port = os.environ.get('PORT', '8000')
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_PORT'] = port
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true'
    ]
    
    subprocess.run(cmd)