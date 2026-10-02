from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agent.service import run_agent


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ToolActivity(BaseModel):
    tool: str
    arguments: dict


class ChatResponse(BaseModel):
    answer: str
    activities: list[ToolActivity]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await run_agent(request.message)

        return ChatResponse(
            answer=result["answer"],
            activities=[
                ToolActivity(**activity)
                for activity in result["activities"]
            ],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {exc}",
        )