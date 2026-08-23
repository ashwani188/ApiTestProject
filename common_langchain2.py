import os
import requests
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

load_dotenv()

# 1. Initialize the correct live Groq Model
llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="groq",
    api_key=os.getenv("GROQ_KEY")
)

@tool
def search(query: str) -> str:
    """Search for information based on the given query."""
    return "tokyo weather is sunny"

@tool
def search_temperature(city: str) -> str:
    """Search for the live, real-time temperature information based on a given city name."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY environment variable is not set."

    geo_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(geo_url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            condition = data["weather"][0]["description"]
            return f"The current temperature in {city} is {temp}°C with {condition}."
        else:
            return f"Could not find weather data for '{city}'. Error: {data.get('message', 'Unknown error')}"

    except Exception as e:
        return f"An error occurred while fetching real-time data: {str(e)}"

# Collection of tools passed into the runtime engine
tools = [search, search_temperature]

# 2. Configure a prompt template that provides the necessary scratchpad space
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Always use the appropriate tool when the user asks about the weather or temperature. Use the `search_temperature` tool for temperature queries."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # Crucial: This allows the model to communicate back-and-forth during execution
])

# 3. Create the modern agent pipeline instead of using legacy initialize_agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    try:
        # Request data natively as a clean input string
        result = agent_executor.invoke({"input": "What is the temperature in patna?"})
        print("\nFinal Result:")
        print(result["output"])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
