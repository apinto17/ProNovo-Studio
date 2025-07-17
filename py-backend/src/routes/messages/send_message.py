from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from agents.agent_graph import get_langgraph_agent, get_test_graph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import ToolMessage
import json

send_message_router = APIRouter()

class message(BaseModel):
    id: int
    sender: str
    content: str
    data: Optional[str]

agent = get_test_graph()

@send_message_router.post("/message-send")
async def send_message(data: message) -> message:
    state = {
        "messages": [HumanMessage(content=data.content)],
        "inputs": {},
        "tool_outputs": []
    }

    result = agent.invoke(state)

    # Extract final PDB data from tool outputs
    pdb_data = None
    for bot_message in result["messages"]:
        if isinstance(bot_message, ToolMessage):
            output = bot_message.content
            if bot_message.name == "rf_diffusion_tool":
                output = json.loads(output)
                pdb_data = output["pdb"]

    return message(
        id=data.id + 1,
        sender="bot",
        content=result["messages"][-1].content if result["messages"] else "Done",
        data=pdb_data
    )