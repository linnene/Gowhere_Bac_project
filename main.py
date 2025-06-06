from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.db import engine
from src.models.base import Base
from src.routers.main_route import api_route 

#-----------在导入模块之后------------
app = FastAPI()  

# Create the database tables

@asynccontextmanager
async def lifespan_expant(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  
    await engine.dispose()

#-----------其他操作之前--------------


# 生命周期
app = FastAPI(lifespan=lifespan_expant)  

#注意位置，需要在life span之后
app.include_router(api_route, prefix="/api")