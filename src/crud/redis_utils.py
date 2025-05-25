import redis.asyncio as redis
from fastapi import HTTPException

#创建redis连接
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

#使用redis储存验证码
async def set_value(key: str, value: str)-> None:
    
    """
    Save Value in Redis
    key: UserId
    value: code
    """
    await redis_client.set(key, value)


async def get_value(key: str):
    value = await redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return value

async def verify_redis_code(code: str, email: str):

    stored_code = await get_value(email)
    return code == stored_code

#Update key value
#TODO: 暂时没有用
async def update_value(key: str, new_value: str):
    exists = await redis_client.exists(key)
    if not exists:
        raise HTTPException(status_code=404, detail="Key not found")
    await redis_client.set(key, new_value)
    return {"message": f"Key '{key}' updated successfully!", "new_value": new_value}


