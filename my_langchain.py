from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from dotenv import load_dotenv
import os
import warnings
from openai import RateLimitError
from langchain_core.messages import HumanMessage

@tool
def search(query: str) -> str:
    """Search for information based on the given query."""
    return "tokyo whether is sunny"

# Suppress LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
tools = [search]
agent = initialize_agent(llm=llm, tools=tools,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Note: LangChain agents are being deprecated in favor of LangGraph. Consider migrating to LangGraph for new use cases.

def main():
    try:
        result = agent.invoke(HumanMessage(content="what is the weather in tokyo"))
        print(result)
    except RateLimitError:
        print("Error: You have exceeded your OpenAI API quota. Please check your plan and billing details.")

if __name__ == "__main__":
    main()
