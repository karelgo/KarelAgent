#!/usr/bin/env python3
"""
Simple test script to validate the Streamlit app components.
This script is used by the CI/CD pipeline to verify functionality.
"""

import sys
import importlib.util
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import streamlit
        import requests
        import fastapi
        import uvicorn
        import pydantic
        print("✓ All core dependencies import successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_streamlit_app():
    """Test that streamlit app module loads."""
    try:
        import streamlit_app
        print("✓ Streamlit app module loads successfully")
        return True
    except Exception as e:
        print(f"✗ Streamlit app error: {e}")
        return False

def test_fastapi_app():
    """Test that FastAPI app module loads."""
    try:
        from main import app
        print("✓ FastAPI app loads successfully")
        return True
    except Exception as e:
        print(f"✗ FastAPI app error: {e}")
        return False

def test_agent_modules():
    """Test that agent modules load."""
    try:
        from agents import DataIngestionAgent, DataCleaningAgent, AnalyticsAgent
        from ceo_agent import ceo_approval_tool
        from base_agent import BaseAgent
        print("✓ Agent modules load successfully")
        return True
    except Exception as e:
        print(f"✗ Agent modules error: {e}")
        return False

def main():
    """Run all tests."""
    print("Running CI/CD validation tests...")
    
    tests = [
        test_imports,
        test_streamlit_app,
        test_fastapi_app,
        test_agent_modules,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    if all(results):
        print("\n✓ All tests passed! The application is ready for deployment.")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())