from typing import Any, TypedDict
from langgraph.graph import StateGraph, END, START
from langchain_core.runnables import RunnableLambda, Runnable
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from agents.tools import rf_diffusion_tool, pdb_search_tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import ToolMessage
from typing import Annotated
from langgraph.graph.message import add_messages

import json
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: list
    inputs: dict
    tool_outputs: list

def create_router_node(llm: ChatOpenAI, tools: list[Tool]):
    llm_with_tools = llm.bind_tools(tools)

    def _router(state: AgentState):
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        if isinstance(response, ToolMessage):
            return {
                **state,
                "messages": messages + [response],
                "tool_outputs": state["tool_outputs"] + [response]
            }
        else:
            return {
              **state,
              "messages": messages + [response]
            }

    return RunnableLambda(_router)


def get_langgraph_agent() -> Runnable:
    llm = ChatOpenAI(model="gpt-4o-mini")
    tools = [pdb_search_tool, rf_diffusion_tool]

    router = create_router_node(llm, tools)
    tool_node = ToolNode(tools=tools)

    builder = StateGraph(AgentState)
    builder.add_node("agent", router)
    builder.add_node("tools", tool_node)

    builder.set_entry_point("agent")
    builder.add_conditional_edges("agent", tools_condition)  # agent → tools
    builder.add_edge("tools", "agent")                       # tools → agent
    builder.set_finish_point("agent")

    graph = builder.compile()
    return graph


class State(TypedDict):
    messages: Annotated[list, add_messages]

def get_test_graph():
  llm = ChatOpenAI(model="gpt-4o-mini")
  graph_builder = StateGraph(State)

  tools = [pdb_search_tool, rf_diffusion_tool]
  llm_with_tools = llm.bind_tools(tools)

  def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

  graph_builder.add_node("chatbot", chatbot)

  tool_node = ToolNode(tools=tools)
  graph_builder.add_node("tools", tool_node)

  graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
  )
  # Any time a tool is called, we return to the chatbot to decide the next step
  graph_builder.add_edge("tools", "chatbot")
  graph_builder.add_edge(START, "chatbot")
  graph = graph_builder.compile()

  return graph