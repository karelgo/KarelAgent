# KarelAgent

Testing personal AI Agents

## DBT Agent Module

A LangChain-powered AI agent module that provides intelligent control over dbt (data build tool) operations through natural language commands.

### Features

- **Natural Language Interface**: Interact with dbt using plain English commands
- **LangChain Integration**: Built on LangChain framework for robust AI agent capabilities
- **Multi-LLM Support**: Works with OpenAI GPT, Anthropic Claude, Azure OpenAI, and other providers
- **Comprehensive dbt Operations**: Supports run, test, list, compile, deps, snapshot, seed, and more
- **Microsoft Fabric Support**: Includes configuration guidance for SQL Analytics and Lakehouse
- **Safety First**: No secrets or credentials committed to repository

### Quick Start

#### Installation

1. Clone this repository:
```bash
git clone https://github.com/karelgo/KarelAgent.git
cd KarelAgent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
# or for other providers:
export ANTHROPIC_API_KEY="your-anthropic-key"
```

#### Basic Usage

```python
from dbt_agent import DBTAgent

# Initialize the agent
agent = DBTAgent()

# Use natural language to control dbt
result = agent.run("List all models in my dbt project")
print(result['response'])

result = agent.run("Run all models in the marts folder")
print(result['response'])

result = agent.run("Test the customer_orders model")
print(result['response'])
```

#### Direct Command Execution

```python
# Execute dbt commands directly
result = agent.execute_dbt_command("run", select="tag:daily")
result = agent.execute_dbt_command("test", models="staging")
```

### Configuration

#### dbt Setup

1. **Initialize a dbt project** (if you don't have one):
```bash
dbt init my_project
cd my_project
```

2. **Configure your `profiles.yml`** file. Default location: `~/.dbt/profiles.yml`

#### Microsoft Fabric Integration

For Microsoft Fabric SQL Analytics Endpoint:
```yaml
# ~/.dbt/profiles.yml
my_project:
  target: prod
  outputs:
    prod:
      type: fabric
      driver: 'ODBC Driver 18 for SQL Server'  
      server: your-fabric-endpoint.datawarehouse.fabric.microsoft.com
      port: 1433
      database: your_database
      schema: dbo
      authentication: ServicePrincipal
      tenant_id: "your-tenant-id"
      client_id: "your-client-id"
      client_secret: "your-client-secret"
      encrypt: true
      trust_cert: false
```

For Microsoft Fabric Lakehouse:
```yaml
# ~/.dbt/profiles.yml  
my_project:
  target: prod
  outputs:
    prod:
      type: fabric
      driver: 'ODBC Driver 18 for SQL Server'
      server: your-lakehouse-endpoint.datawarehouse.fabric.microsoft.com
      port: 1433
      database: your_lakehouse
      schema: dbo
      authentication: ActiveDirectoryInteractive
      # or use Service Principal authentication as above
```

#### Other Database Configurations

**PostgreSQL:**
```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      password: "{{ env_var('DB_PASSWORD') }}"
      port: 5432
      dbname: analytics
      schema: public
```

**Snowflake:**
```yaml
my_project:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: your_account
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: analyst
      database: analytics
      warehouse: compute_wh
      schema: public
```

### Multi-LLM Provider Support

#### OpenAI (Default)
```python
from dbt_agent import create_dbt_agent

agent = create_dbt_agent(
    llm_provider="openai",
    api_key="your-openai-key",
    model_name="gpt-4"
)
```

#### Anthropic Claude
```python
agent = create_dbt_agent(
    llm_provider="anthropic", 
    api_key="your-anthropic-key",
    model_name="claude-3-sonnet-20240229"
)
```

#### Azure OpenAI
```python
agent = create_dbt_agent(
    llm_provider="azure",
    api_key="your-azure-key",
    model_name="gpt-35-turbo",
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_version="2023-05-15"
)
```

#### Custom LLM Provider
```python
from langchain_community.llms import YourCustomLLM

custom_llm = YourCustomLLM(api_key="your-key")
agent = DBTAgent(llm=custom_llm)
```

### Advanced Usage

#### Project-Specific Configuration
```python
agent = DBTAgent(
    project_dir="/path/to/your/dbt/project",
    profiles_dir="/path/to/your/profiles",
    verbose=True
)
```

#### Health Check
```python
health = agent.health_check()
if health['success']:
    print("dbt project is ready!")
else:
    print(f"Issues found: {health['error']}")
```

#### Example Natural Language Commands

- "Run all staging models"
- "Test models that have changed since yesterday" 
- "List models in the marts folder"
- "Run a full refresh on the customer_orders table"
- "Install dbt dependencies"
- "Compile all models without running them"
- "Run snapshots for customer data"
- "Load seed data into the database"

### API Reference

#### DBTAgent Class

**Constructor:**
```python
DBTAgent(
    llm=None,                    # Pre-configured LLM instance
    openai_api_key=None,         # OpenAI API key
    model_name="gpt-3.5-turbo",  # Model name
    temperature=0.1,             # LLM temperature
    project_dir=None,            # dbt project directory
    profiles_dir=None,           # dbt profiles directory
    verbose=False                # Enable verbose logging
)
```

**Methods:**
- `run(query: str, chat_history: List = None) -> Dict`: Process natural language query
- `execute_dbt_command(command: str, **kwargs) -> Dict`: Execute dbt command directly
- `health_check() -> Dict`: Check dbt project health
- `get_available_commands() -> List[str]`: Get supported dbt commands

#### DBTTool Class

LangChain tool for dbt CLI operations.

**Supported Commands:**
- `run`: Execute dbt models
- `test`: Run dbt tests  
- `list`: List available models
- `compile`: Compile models without execution
- `deps`: Install dependencies
- `snapshot`: Run snapshots
- `seed`: Load seed data
- `clean`: Clean dbt artifacts
- `debug`: Debug dbt configuration
- `docs`: Generate documentation

### Environment Variables

Set these environment variables for different providers:

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Azure OpenAI
export AZURE_OPENAI_API_KEY="your-azure-openai-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"

# Database credentials (use dbt profiles instead when possible)
export DB_PASSWORD="your-db-password"
export SNOWFLAKE_USER="your-snowflake-user"
export SNOWFLAKE_PASSWORD="your-snowflake-password"
```

### Security Best Practices

1. **Never commit API keys or credentials** to version control
2. **Use environment variables** for sensitive configuration
3. **Use dbt profiles** for database credentials
4. **Set appropriate permissions** on profiles.yml file (`chmod 600 ~/.dbt/profiles.yml`)
5. **Use service principals** for production deployments
6. **Rotate keys regularly** and monitor usage

### Troubleshooting

#### Common Issues

**"dbt command not found"**
- Ensure dbt-core is installed: `pip install dbt-core`
- Verify dbt is in your PATH: `which dbt`

**"Could not find profile"**
- Check your profiles.yml location: `~/.dbt/profiles.yml`
- Verify profile name matches your dbt_project.yml
- Run `dbt debug` to diagnose connection issues

**"OpenAI API key not found"**
- Set the OPENAI_API_KEY environment variable
- Or pass the key directly to DBTAgent constructor

**"Models not found"**
- Ensure you're in the correct dbt project directory
- Check that models exist: `dbt list`
- Verify project configuration in dbt_project.yml

#### Getting Help

- Check dbt documentation: https://docs.getdbt.com/
- Review LangChain docs: https://python.langchain.com/
- Open an issue on this repository for bugs or feature requests

### Extension and Customization

#### Adding New LLM Providers

1. Install the provider's LangChain integration
2. Extend the `create_dbt_agent()` factory function
3. Follow the pattern in `agent.py` for provider-specific configuration

#### Custom dbt Commands

Extend the `DBTTool` class to add support for dbt plugins or custom commands:

```python
class CustomDBTTool(DBTTool):
    def _run(self, command: str, **kwargs):
        if command == "custom_command":
            # Handle your custom logic
            pass
        return super()._run(command, **kwargs)
```

#### Custom Agent Prompts

Modify the system prompt in `DBTAgent` to customize the agent's behavior:

```python
agent = DBTAgent()
agent.system_prompt = "Your custom prompt here..."
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable  
5. Submit a pull request

### License

MIT License - see LICENSE file for details.
