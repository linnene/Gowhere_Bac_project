from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers.main_route import api_route 


#-----------在导入模块之后------------
app = FastAPI()  

# Create the database tables
# 数据库操作

#-----------其他操作之前--------------


# 生命周期
# app = FastAPI(lifespan=lifespan_expant)  


#注意位置，需要在life span之后
app.include_router(api_route, prefix="/api")