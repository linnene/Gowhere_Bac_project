from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dp import chat_loop_block,get_chat_by_id
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
    
@router.get("/chat_history")
async def chat_history(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户聊天历史
    """
    try:
        chat = await get_chat_by_id(user_id,db)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))