
# BaseAgent is now a simple class, not a LangChain Agent subclass
class BaseAgent:
    def __init__(self, name, ceo_tool):
        self.name = name
        self.ceo_tool = ceo_tool

    def request_approval(self, action):
        return self.ceo_tool(action)
