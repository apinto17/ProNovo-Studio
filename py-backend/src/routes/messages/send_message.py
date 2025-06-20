from fastapi import APIRouter
from pydantic import BaseModel

send_message_router = APIRouter()

class message(BaseModel):
    id: int
    sender: str
    content: str

@send_message_router.post("/message-send")
async def send_message(data: message) -> message:
    print(data.content)
    return message(id=data.id + 1, sender="bot", content="hello from chat bot")