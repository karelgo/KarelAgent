"""
DBT Agent with LangChain integration.

This module provides the main agent logic for interpreting natural language
queries and executing dbt commands using LangChain and Large Language Models.
"""

import os
from typing import Optional, List, Dict, Any, Union
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.base import BaseLanguageModel

from .dbt_tool import DBTTool, create_dbt_tool


class DBTAgent:
    """
    A LangChain-powered AI agent for controlling dbt operations through natural language.
    
    This agent can interpret user queries about dbt operations and execute the
    appropriate dbt commands using the DBTTool.
    """
    
    def __init__(self,
                 llm: Optional[BaseLanguageModel] = None,
                 openai_api_key: Optional[str] = None,
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.1,
                 project_dir: Optional[str] = None,
                 profiles_dir: Optional[str] = None,
                 verbose: bool = False):
        """
        Initialize the DBT Agent.
        
        Args:
            llm: Pre-configured language model instance. If None, creates OpenAI ChatGPT
            openai_api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var
            model_name: Name of the model to use (default: gpt-3.5-turbo)
            temperature: Temperature for LLM responses (default: 0.1 for consistency)
            project_dir: Default dbt project directory
            profiles_dir: Default dbt profiles directory  
            verbose: Whether to enable verbose logging
        """
        
        # Initialize the language model
        if llm is None:
            if openai_api_key is None:
                openai_api_key = os.getenv("OPENAI_API_KEY")
                if not openai_api_key:
                    raise ValueError(
                        "OpenAI API key must be provided either through openai_api_key parameter "
                        "or OPENAI_API_KEY environment variable"
                    )
            
            self.llm = ChatOpenAI(
                api_key=openai_api_key,
                model=model_name,
                temperature=temperature
            )
        else:
            self.llm = llm
        
        # Create dbt tool
        self.dbt_tool = create_dbt_tool(project_dir=project_dir, profiles_dir=profiles_dir)
        self.tools = [self.dbt_tool]
        
        # Define the system prompt
        self.system_prompt = """
You are a helpful AI assistant specialized in dbt (data build tool) operations. 
You can help users with their dbt projects by executing dbt commands through natural language.

Your capabilities include:
- Running dbt models (dbt run)
- Testing dbt models (dbt test) 
- Listing available models (dbt list)
- Compiling dbt models (dbt compile)
- Installing dependencies (dbt deps)
- Running snapshots (dbt snapshot)
- Loading seed data (dbt seed)

When users ask about dbt operations:
1. Understand what they want to accomplish
2. Use the dbt_tool to execute the appropriate dbt command
3. Interpret the results and provide helpful feedback
4. Suggest next steps or additional actions if relevant

Always be specific about what dbt command you're running and explain the results clearly.
If a command fails, help diagnose the issue and suggest solutions.

Guidelines:
- For model selection, use dbt's selection syntax (e.g., tag:daily, +my_model+, path:marts/)
- Consider dependencies when running models
- Suggest testing after running models
- Be aware of performance implications for large projects
- Recommend incremental runs vs full refreshes appropriately
"""

        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        # Create the agent
        self.agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt_template
        )
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def run(self, query: str, chat_history: Optional[List] = None) -> Dict[str, Any]:
        """
        Process a natural language query about dbt operations.
        
        Args:
            query: Natural language query about dbt operations
            chat_history: Optional chat history for context
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            result = self.agent_executor.invoke({
                "input": query,
                "chat_history": chat_history or []
            })
            
            return {
                "success": True,
                "response": result["output"],
                "input": query,
                "intermediate_steps": result.get("intermediate_steps", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Error processing query: {str(e)}",
                "input": query,
                "error": str(e)
            }
    
    def execute_dbt_command(self, 
                           command: str,
                           **kwargs) -> Dict[str, Any]:
        """
        Directly execute a dbt command without natural language processing.
        
        Args:
            command: dbt command to execute
            **kwargs: Additional arguments for the dbt command
            
        Returns:
            Dictionary containing the command result
        """
        try:
            result = self.dbt_tool._run(command=command, **kwargs)
            return {
                "success": True,
                "result": result,
                "command": command,
                "arguments": kwargs
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "arguments": kwargs
            }
    
    def get_available_commands(self) -> List[str]:
        """
        Get list of available dbt commands.
        
        Returns:
            List of supported dbt commands
        """
        return [
            "run", "test", "list", "compile", "deps", 
            "snapshot", "seed", "clean", "debug", "docs"
        ]
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the dbt project.
        
        Returns:
            Dictionary containing health check results
        """
        try:
            # Test dbt debug command
            debug_result = self.execute_dbt_command("debug")
            
            # Test listing models
            list_result = self.execute_dbt_command("list", select="*")
            
            return {
                "success": True,
                "dbt_debug": debug_result,
                "model_list": list_result,
                "message": "dbt project appears to be configured correctly"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Issues detected with dbt project configuration"
            }


def create_dbt_agent(llm_provider: str = "openai",
                    api_key: Optional[str] = None,
                    model_name: Optional[str] = None,
                    **kwargs) -> DBTAgent:
    """
    Factory function to create a DBT agent with different LLM providers.
    
    Args:
        llm_provider: LLM provider ("openai", "anthropic", "azure", etc.)
        api_key: API key for the provider
        model_name: Model name to use
        **kwargs: Additional arguments for DBTAgent
        
    Returns:
        Configured DBTAgent instance
        
    Raises:
        ValueError: If unsupported provider or missing configuration
    """
    
    if llm_provider.lower() == "openai":
        model_name = model_name or "gpt-3.5-turbo"
        return DBTAgent(
            openai_api_key=api_key,
            model_name=model_name,
            **kwargs
        )
    
    elif llm_provider.lower() == "azure":
        # Azure OpenAI configuration
        from langchain_openai import AzureChatOpenAI
        
        if not all([api_key, model_name]):
            raise ValueError("Azure provider requires api_key and model_name")
            
        azure_endpoint = kwargs.pop('azure_endpoint', None)
        api_version = kwargs.pop('api_version', '2023-05-15')
        
        if not azure_endpoint:
            raise ValueError("Azure provider requires azure_endpoint")
            
        llm = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version,
            deployment_name=model_name,
            temperature=kwargs.get('temperature', 0.1)
        )
        
        return DBTAgent(llm=llm, **kwargs)
    
    elif llm_provider.lower() == "anthropic":
        # Anthropic Claude configuration
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            raise ImportError("langchain_anthropic required for Anthropic provider")
            
        model_name = model_name or "claude-3-sonnet-20240229"
        llm = ChatAnthropic(
            api_key=api_key,
            model=model_name,
            temperature=kwargs.get('temperature', 0.1)
        )
        
        return DBTAgent(llm=llm, **kwargs)
    
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")


# Example usage and testing functions
def example_usage():
    """Example usage of the DBT Agent."""
    
    # Basic usage with OpenAI
    agent = DBTAgent()
    
    # Example queries
    queries = [
        "List all models in my dbt project",
        "Run all models in the marts folder", 
        "Test the customer_orders model",
        "What's the status of my dbt project?",
        "Run a full refresh on staging models"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = agent.run(query)
        print(f"Response: {result['response']}")
        

if __name__ == "__main__":
    # Run example if script is executed directly
    example_usage()