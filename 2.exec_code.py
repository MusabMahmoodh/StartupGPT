import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub
from utils.safety import SandboxedPythonREPLTool
from utils.github_tools import GitHubCreateRepoTool
from workflows.debate import build_workflow, DebateState

# Initialize core components
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Configure tools
tools = [
    DuckDuckGoSearchRun(),
    SandboxedPythonREPLTool(),
    GitHubCreateRepoTool()
]

# Build agents
main_agent = create_tool_calling_agent(llm, tools, hub.pull("hwchase17/openai-tools-agent"))
main_executor = AgentExecutor(agent=main_agent, tools=tools, verbose=True)

# Build debate system
debate_workflow = build_workflow(tools).compile()

# Example usage
if __name__ == "__main__":
    # Single-agent task
    code_result = main_executor.invoke({
        "input": "Create a Python script that checks cryptocurrency prices"
    })
    print("\nCode Result:", code_result['output'])
    
    # Multi-agent debate
    debate_result = debate_workflow.invoke({
        "task": "Should we add Web3 features to attract investors?",
        "messages": []
    })
    print("\nDebate Log:", debate_result['messages'])