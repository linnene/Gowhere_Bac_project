from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends ,HTTPException,Query
from ..db.db import get_db
from typing import Annotated

from ..schemas.user import UserRead, UserUpdate
from ..crud.user_db import get_user_by_id,reflush_user,get_user_by_email

router = APIRouter()

@router.post(
"/Login_user",
response_model = UserRead
)
async def login_user(
    userpassword: str,
    db: Annotated[AsyncSession , Depends(get_db)],
    userid: str = Query(default=None),
    useremail: str = Query(default=None)
    ):
    
    """
        登录主接口：
        args:
        UserId: str
        UserPassword: str
        UserEmail: str

        应该返回tokens，refresh和Access Token ，还有User Info
    """

    if  not userid and not useremail:
        raise HTTPException(400,"邮箱与ID至少需要一个") 
    elif not userpassword:
        raise HTTPException(400,"需要密码")
    
    curr_user = await get_user_by_id(userid,db) or get_user_by_email(userid,db)
    if curr_user.UserPassword == userpassword:
        #reture refresh和Access Token:
        
        pass







@router.put(
"/update_user",
# response_model= UserRead
)
async def update_user(
    user_id: str,
    new_user: UserUpdate,
    db: Annotated[AsyncSession , Depends(get_db)]
    ):
    
    #BUG: 使用接口Updateuser无法找到用户
    #TODO： 更新用户信息

    user = await reflush_user(new_user, user_id, db)
    return user

