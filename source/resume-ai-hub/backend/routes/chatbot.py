import os
import anthropic
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

router = APIRouter()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class Message(BaseModel):
    role: str
    content: str


class ChatInput(BaseModel):
    messages: List[Message]


SYSTEM_PROMPT = """You are CareerCoach AI, an expert career advisor and HR professional with deep expertise in:
- Resume writing and optimization
- Job searching strategies
- Interview preparation and coaching
- Salary negotiation
- Career transitions and pivots
- LinkedIn profile optimization
- Professional development and upskilling
- Industry trends and job market insights

You provide personalized, practical, and actionable career advice. You are encouraging, honest, and data-driven.
When giving advice, always tailor it to the specific situation described by the user.
Keep responses concise but comprehensive. Use bullet points and formatting when it helps clarity."""


@router.post("/chat")
async def chat(data: ChatInput):
    messages = [{"role": m.role, "content": m.content} for m in data.messages]

    def generate():
        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")
