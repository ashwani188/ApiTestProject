from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

llm = init_chat_model(model="openai/gpt-oss-20b",model_provider="groq", api_key=os.getenv("GROQ_KEY"))

response = llm.invoke("what is langchain?")
print(response.content)