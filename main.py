from fastapi import FastAPI
from pydantic import BaseModel
from router import detect_route
from memory import load_memory, save_memory
from Agents.tech_agent import agent
import uvicorn


app = FastAPI()

class ChatRequest(BaseModel):
    session_id: int
    user_id: int
    message: str

@app.post("/v1/chat/completions")
def chat(request: ChatRequest):
    user_msg = request.message

    reply = detect_route(user_msg)
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": reply
                }
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)