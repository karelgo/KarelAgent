"""
DBT Tool for LangChain integration.

This module provides a LangChain Tool that wraps dbt CLI operations,
allowing AI agents to execute dbt commands like run, test, and list models.
"""

import subprocess
import json
from typing import Optional, List, Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class DBTToolInput(BaseModel):
    """Input for DBT Tool."""
    command: str = Field(description="dbt command to execute (run, test, list, compile, etc.)")
    models: Optional[str] = Field(default=None, description="Specific models to target (space-separated)")
    select: Optional[str] = Field(default=None, description="dbt selection syntax for models")
    exclude: Optional[str] = Field(default=None, description="Models to exclude")
    full_refresh: bool = Field(default=False, description="Whether to perform full refresh")
    fail_fast: bool = Field(default=False, description="Stop execution on first failure")
    project_dir: Optional[str] = Field(default=None, description="dbt project directory")
    profiles_dir: Optional[str] = Field(default=None, description="dbt profiles directory")


class DBTTool(BaseTool):
    """A LangChain tool for executing dbt commands."""
    
    name: str = "dbt_tool"
    description: str = """
    Execute dbt (data build tool) commands. This tool can run dbt operations like:
    - 'run': Execute dbt models
    - 'test': Run dbt tests
    - 'list': List available models
    - 'compile': Compile dbt models without executing
    - 'deps': Install dbt dependencies
    - 'snapshot': Run dbt snapshots
    - 'seed': Load seed data
    
    Use this tool when you need to interact with a dbt project.
    """
    args_schema = DBTToolInput
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _run(self, 
             command: str,
             models: Optional[str] = None,
             select: Optional[str] = None,
             exclude: Optional[str] = None,
             full_refresh: bool = False,
             fail_fast: bool = False,
             project_dir: Optional[str] = None,
             profiles_dir: Optional[str] = None) -> str:
        """Execute a dbt command and return the result."""
        
        # Build the dbt command
        dbt_cmd = ["dbt", command]
        
        # Add model selection options
        if models:
            dbt_cmd.extend(["--models", models])
        elif select:
            dbt_cmd.extend(["--select", select])
            
        if exclude:
            dbt_cmd.extend(["--exclude", exclude])
            
        # Add flags
        if full_refresh:
            dbt_cmd.append("--full-refresh")
        if fail_fast:
            dbt_cmd.append("--fail-fast")
            
        # Add directory options
        if project_dir:
            dbt_cmd.extend(["--project-dir", project_dir])
        if profiles_dir:
            dbt_cmd.extend(["--profiles-dir", profiles_dir])
            
        try:
            # Execute the command
            result = subprocess.run(
                dbt_cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Format the response
            output = {
                "command": " ".join(dbt_cmd),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
            # For list commands, try to parse JSON output
            if command == "list" and result.returncode == 0:
                try:
                    # dbt list can output JSON with --output json flag
                    if "--output" not in dbt_cmd:
                        # Re-run with JSON output for better parsing
                        json_cmd = dbt_cmd + ["--output", "json"]
                        json_result = subprocess.run(
                            json_cmd,
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        if json_result.returncode == 0:
                            output["json_output"] = json_result.stdout
                except Exception:
                    pass  # Fall back to regular output
            
            return json.dumps(output, indent=2)
            
        except subprocess.TimeoutExpired:
            return json.dumps({
                "command": " ".join(dbt_cmd),
                "error": "Command timed out after 5 minutes",
                "success": False
            }, indent=2)
        except Exception as e:
            return json.dumps({
                "command": " ".join(dbt_cmd),
                "error": f"Error executing command: {str(e)}",
                "success": False
            }, indent=2)


def create_dbt_tool(project_dir: Optional[str] = None, 
                   profiles_dir: Optional[str] = None) -> DBTTool:
    """
    Factory function to create a DBT tool with default project and profiles directories.
    
    Args:
        project_dir: Default dbt project directory
        profiles_dir: Default dbt profiles directory
        
    Returns:
        Configured DBTTool instance
    """
    class ConfiguredDBTTool(DBTTool):
        def _run(self, **kwargs):
            # Override with defaults if not provided
            if project_dir and not kwargs.get('project_dir'):
                kwargs['project_dir'] = project_dir
            if profiles_dir and not kwargs.get('profiles_dir'):
                kwargs['profiles_dir'] = profiles_dir
            return super()._run(**kwargs)
    
    return ConfiguredDBTTool()