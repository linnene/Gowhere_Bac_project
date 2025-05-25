from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dp import chat_loop_block
from src.db.db import get_db

router = APIRouter()

@router.get("/chat")
async def chat(
    user_id: str,
    message: str,
    db: AsyncSession = Depends(get_db),
):
    """
    聊天接口
    """
    try:
        response = await chat_loop_block(message,user_id,db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))