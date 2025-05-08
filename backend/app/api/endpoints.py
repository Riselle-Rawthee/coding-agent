from fastapi import APIRouter, HTTPException
import ollama
from core.errors import CustomHTTPException
from api.models import CodeGenerationRequest, ChatMessage, ChatHistory
from typing import Dict
from typing import List

router = APIRouter()

# In-memory storage for chat history
chat_history: Dict[str, List[ChatMessage]] = {}

@router.get("/models")
async def list_models():
    try:
        models = ollama.list()
        return {"models": models}
    except Exception as e:
        raise CustomHTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_code(request: CodeGenerationRequest):
    try:
        session_id = request.session_id

        # Initialize chat history if it doesn't exist
        if session_id not in chat_history:
            chat_history[session_id] = []

        # Add the user's message to the chat history
        chat_history[session_id].append(ChatMessage(role="user", content=request.prompt))

        # Prepare the full conversation for the model
        conversation = [{"role": msg.role, "content": msg.content} for msg in chat_history[session_id]]

        # Generate a response using the model
        response = ollama.chat(model=request.model, messages=conversation)

        # Add the assistant's response to the chat history
        chat_history[session_id].append(ChatMessage(role="assistant", content=response["message"]["content"]))

        return {"response": response["message"]["content"]}
    except Exception as e:
        raise CustomHTTPException(status_code=500, detail=str(e))