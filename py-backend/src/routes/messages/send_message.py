from typing import Optional
from fastapi import APIRouter
from agents.schemas import ToolOutputCaptureHandler
from agents.schemas import ProteinDesignResult
from pydantic import BaseModel, ValidationError
from agents.agent import Agent

send_message_router = APIRouter()

class message(BaseModel):
    id: int
    sender: str
    content: str
    data: Optional[str]

@send_message_router.post("/message-send")
async def send_message(data: message) -> message:
    agent = Agent.get_agent()
    handler = ToolOutputCaptureHandler()
    response = await agent.ainvoke({"input": data.content}, config={"callbacks": [handler]})

    # Check if the tool output is present
    pdb_data = None
    for output in handler.tool_outputs:
        print(output)
        if isinstance(output, dict) and "pdb" in output:
            pdb_data = output["pdb"]

    print(response)

    return message(
        id=data.id + 1,
        sender="bot",
        content=response["output"],
        data=pdb_data
    )