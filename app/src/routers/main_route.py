from fastapi import APIRouter
from . import email , login ,signup

api_route = APIRouter(prefix="/v1",tags=["V1"])

api_route.include_router(email.router, prefix="/email", tags=["EMAIL"])
api_route.include_router(login.router, prefix="/Login", tags=["Login"])
api_route.include_router(signup.router, prefix="/Signup", tags=["Signup"])