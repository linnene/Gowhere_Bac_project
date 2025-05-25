from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json

from src.models.user import User
from src.schemas.user import UserCreate,UserUpdate
from .base import hash_password, verify_password

async def create_user(user: UserCreate, db: AsyncSession) -> User:

    """
    有关创建一个新的用户，现在的用户ID又数据库自己创建，
    之后会将ID改为PhoneNumber将账号和手机号绑定
    TODO：修改 {User} 中的 ID 表项
    """
    async with db.begin():  # 开启事务

        result = await db.execute(select(User).filter(User.UserId == user.UserId))
        
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="User already registered")
        
        user.UserPassword = hash_password(user.UserPassword)  
        
        new_user = User(**user.model_dump())
        db.add(new_user)
        await db.flush()

    # TODO:如果数据库字段不会自动填充（如 created_at），可以不 refresh()，提升性能。
    # await db.refresh(new_user)
    return new_user

async def get_user_by_email(email: str, db: AsyncSession) -> User:

    """
    通过邮箱获取用户信息
    """

    result = await db.execute(select(User).filter(User.UserEmail == email))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_user_by_id(user_id: str, db: AsyncSession):

    """
    通过用户ID获取用户信息
    """

    result = await db.execute(select(User).filter(User.UserId == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

async def reflush_user(new_user: UserUpdate ,user_id: str ,db: AsyncSession):

    """
    更新用户信息
    TODO: 验证是否异步
    """
    
    async with db.begin():
        cur_user = await get_user_by_id(user_id, db) 
        if cur_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        print(cur_user)
        cur_user.UserName = new_user.UserName
        cur_user.UserPassword = new_user.UserPassword
        cur_user.UserEmail = new_user.UserEmail
        cur_user.Is_Ban = new_user.Is_Ban
        await db.flush()
        
    return cur_user

async def reflush_user_chat(user_id: str, db: AsyncSession, chat: list[dict]):
    cur_user = await get_user_by_id(user_id, db)
    if cur_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    cur_user.ChatHistory = json.dumps(chat)
    await db.flush()    # 刷新到数据库
    await db.commit()   # 提交事务，确保保存

    return cur_user



#TODO:返回值有待商榷
async def verify_user_by_pw(user_id: str, password: str, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not verify_password(password, user.UserPassword):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user

async def set_user_emaliVer(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if user:
        user.UserEmailVerified = True
        await db.commit()

#TODO: 完成
async def delete_users(user_ids: list[str], db: AsyncSession):
    pass