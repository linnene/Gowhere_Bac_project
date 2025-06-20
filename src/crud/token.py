from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException

from config import settings
from .user_db import get_user_by_id

async def encode_refresh_token(UserId:str,db:AsyncSession): 
    """
        使用id查询User:
            UserId: str
            db: AsyncSession
        
        func:
            编码refreshtoken
        
        return:
            refreshToken
    """

    # 获取当前 UTC 时间
    curr_time =datetime.now(timezone.utc)
    expire_time = curr_time + timedelta(minutes=settings.refresh_token_expire_minutes)

    curr_user = await get_user_by_id(UserId,db)
    if not curr_user:
        raise HTTPException(status_code=400, detail="User not found")

    header={
        'typ': 'refresh_token',
        'alg': 'HS256',
    }

    payload = {
        'sub': UserId,  # subject (用户标识)
        'iat': int(curr_time.timestamp()),  # issued at (令牌创建时间)
        'exp': int(expire_time.timestamp()),  # expires at (令牌过期时间)
    }

    refresh_token = jwt.encode(
        payload,
        settings.token_secret_key,
        algorithm='HS256',
        headers=header
    )

    return refresh_token

async def encode_access_token(UserId:str,db:AsyncSession):
    """
        使用id查询User:
            UserId: str
            db: AsyncSession
        func:
            编码accesstoken
        return:
            accessToken  
    """

    # 获取当前 UTC 时间
    curr_time =datetime.now(timezone.utc)
    expire_time = curr_time + timedelta(minutes=settings.access_token_expire_minutes)

    curr_user = await get_user_by_id(UserId,db)
    if not curr_user:
        raise HTTPException(status_code=400, detail="User not found")

    header={
        'typ': 'access_token',
        'alg': 'HS256',
    }

    payload = {
        'sub': UserId,  # subject (用户标识)
        'iat': int(curr_time.timestamp()),  # issued at (令牌创建时间)
        'exp': int(expire_time.timestamp()),  # expires at (令牌过期时间)
    }

    access_token = jwt.encode(
        payload,
        settings.token_secret_key,
        algorithm='HS256',
        headers=header
    )

    return access_token

async def v_refresh_token(refresh_token: str):
    """
    验证 refreshToken
    """
    try:
        payload = jwt.decode(refresh_token, settings.token_secret_key, algorithms=['HS256'])
        if payload['exp'] < int(datetime.now(timezone.utc).timestamp()):
            raise HTTPException(status_code=400, detail="refreshToken 已经过期")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="refreshToken 已经过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="无效的 refreshToken")

async def v_access_token(access_token: str):
    """
    验证 accessToken
    """
    try:
        payload = jwt.decode(access_token, settings.token_secret_key, algorithms=['HS256'])
        if payload['exp'] < int(datetime.now(timezone.utc).timestamp()):
            raise HTTPException(status_code=400, detail="accessToken 已经过期")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="accessToken 已经过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="无效的 accessToken")