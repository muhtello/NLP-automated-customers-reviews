from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from bot_engine import PersonaChatbot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Shopping Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wichtig: Verhindert, dass sein Frontend geblockt wird
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = PersonaChatbot()


# Schema für einzelne Nachrichten
class Message(BaseModel):
    role: str  # "user" oder "assistant"
    content: str


# Schema für die Anfrage
class ChatRequest(BaseModel):
    user_message: str
    category_file: str
    mode: str = "recommender"
    history: Optional[List[Message]] = []


@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    reply = bot.generate_response(
        user_message=request.user_message,
        category_file=request.category_file,
        mode=request.mode,
        history=request.history,
    )
    return {"response": reply}