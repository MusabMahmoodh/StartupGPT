from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain import hub
import os
from dotenv import load_dotenv

# Load OpenAI key
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Define tools
tools = [DuckDuckGoSearchRun()]

# Create agent
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent!
response = agent_executor.invoke({
    "input": "Create a Flask API endpoint for text summarization."
})

print(response["output"])
