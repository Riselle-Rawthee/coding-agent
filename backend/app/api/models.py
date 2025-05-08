from pydantic import BaseModel
from typing import List, Dict

class CodeGenerationRequest(BaseModel):
    model: str
    prompt: str
    session_id: str  # Unique ID for each chat session

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]