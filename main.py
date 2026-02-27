from typing import List, Optional, Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict
from router import detect_route
from memory import load_memory, save_memory
from agent_manager import get_agent
import uvicorn
import time
import json


app = FastAPI()


def make_response(content: str):
    return {
        "id": "chatcmpl-local",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "bfiber-agent",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }


def make_stream_response(content: str):
    """Generate SSE stream chunks in OpenAI format for LibreChat."""
    # First chunk: send role
    chunk_role = {
        "id": "chatcmpl-local",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "bfiber-agent",
        "choices": [
            {
                "index": 0,
                "delta": {"role": "assistant", "content": ""},
                "finish_reason": None
            }
        ]
    }
    yield f"data: {json.dumps(chunk_role)}\n\n"

    # Second chunk: send content
    chunk_content = {
        "id": "chatcmpl-local",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "bfiber-agent",
        "choices": [
            {
                "index": 0,
                "delta": {"content": content},
                "finish_reason": None
            }
        ]
    }
    yield f"data: {json.dumps(chunk_content)}\n\n"

    # Final chunk: finish
    chunk_done = {
        "id": "chatcmpl-local",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "bfiber-agent",
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }
        ]
    }
    yield f"data: {json.dumps(chunk_done)}\n\n"
    yield "data: [DONE]\n\n"


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="allow")
    role: str
    content: Optional[Union[str, list]] = ""

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    model: str
    user: Optional[str] = None
    stream: Optional[bool] = None
    messages: List[ChatMessage]


# Catch validation errors → return valid response instead of 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"[VALIDATION ERROR] {exc}")
    return JSONResponse(
        status_code=200,
        content=make_response("Maaf, terjadi kesalahan pada format request.")
    )

@app.get("/v1/models")
def models():
    return {
        "data": [
            {
                "id": "bfiber-agent",
                "object": "model",
            }
        ]
    }


def _get_ai_content(request: ChatRequest):
    """Process the request and return the AI content string."""
    chat_msg = request.messages[-1]
    content = chat_msg.content
    if isinstance(content, list):
        user_msg = ""
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                user_msg += part.get("text", "")
    else:
        user_msg = content or ""
    session = request.user or "librechat-session"
    history = load_memory(session)
    user_id = 1

    # Build context from recent messages (last 6 messages, excluding current)
    recent_messages = request.messages[-7:-1] # 6 messages before current message
    context = []
    for msg in recent_messages:
        msg_content = msg.content
        if isinstance(msg_content, list):
            text = ""
            for part in msg_content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text += part.get("text", "")
            msg_content = text
        context.append({"role": msg.role, "content": msg_content or ""})

    reply = detect_route(user_msg, context=context if context else None)
    agent = get_agent(reply)

    if agent is None:
        return "Maaf, saat ini saya hanya bisa membantu dengan masalah mengenai BFiber. Silakan hubungi call center BFiber untuk masalah lain."

    try:
        response = agent.run(user_msg, history)
        message = response.get("messages", [])

        if message:
            last_msg = message[-1]
            if hasattr(last_msg, "content"):
                ai_content = last_msg.content
            else:
                ai_content = str(last_msg)
        else:
            ai_content = ""

        save_memory(session, user_id, "user", user_msg)
        save_memory(session, user_id, "assistant", str(ai_content))
        return str(ai_content)

    except Exception as e:
        print(f"[ERROR] {e}")
        return f"Maaf, terjadi kesalahan internal: {str(e)}"


@app.post("/v1/chat/completions")
def chat(request: ChatRequest):
    ai_content = _get_ai_content(request)

    if request.stream:
        return StreamingResponse(
            make_stream_response(ai_content),
            media_type="text/event-stream"
        )
    else:
        return make_response(ai_content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)