from langgraph.graph import StateGraph
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain import hub

class DebateState(TypedDict):
    messages: List[str]
    task: str

def create_debate_agent(tools, role_prompt: str):
    llm = ChatOpenAI(model="gpt-4-turbo")
    agent = create_tool_calling_agent(
        llm,
        tools,
        hub.pull("hwchase17/openai-tools-agent").partial(system_message=role_prompt)
    )
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

def build_workflow(tools):
    # Create agents
    ceo_agent = create_debate_agent(
        tools,
        "You are a startup CEO focused on rapid growth. Prioritize speed over perfection."
    )
    
    dev_agent = create_debate_agent(
        tools,
        "You are a senior developer. Prevent technical debt at all costs."
    )

    # Define nodes
    def ceo_node(state: DebateState):
        response = ceo_agent.invoke({"input": state["task"]})
        return {"messages": [f"CEO: {response['output']}"]}
    
    def dev_node(state: DebateState):
        response = dev_agent.invoke({"input": state["task"]})
        return {"messages": [f"Developer: {response['output']}"]}

    # Build graph
    workflow = StateGraph(DebateState)
    workflow.add_node("ceo", ceo_node)
    workflow.add_node("developer", dev_node)
    workflow.add_edge("ceo", "developer")
    workflow.set_entry_point("ceo")
    
    return workflow