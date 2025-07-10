from pydantic import BaseModel
from typing import Optional
from langchain.callbacks.base import BaseCallbackHandler

class ToolOutputCaptureHandler(BaseCallbackHandler):
    def __init__(self):
        self.tool_outputs = []

    def on_tool_end(self, output, **kwargs):
        self.tool_outputs.append(output)

class ProteinDesignResult(BaseModel):
    message: str
    pdb: Optional[str] = None