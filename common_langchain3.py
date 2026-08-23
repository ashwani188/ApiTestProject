from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain_core.tools import tool

load_dotenv()
llm=init_chat_model(model="openai/gpt-oss-20b", model_provider="groq", api_key=os.getenv("GROQ_KEY"))

@tool
def get_weather():
    """Get the current weather information."""
    return "The current weather is sunny."

message=ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Always use the appropriate tool when the user asks about the weather or temperature. Use the `get_weather` tool for temperature queries."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")])
# Crucial: This allows the model to communicate back-and-forth during execution

tools = [get_weather]

agent= create_tool_calling_agent(llm, tools, message)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    result=agent_executor.invoke({"input": "what is the weather in tokyo"})
    print(result)

if __name__=="__main__":
    main()
