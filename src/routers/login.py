from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends ,HTTPException,Query
from typing import Annotated

from ..db.db import get_db
from ..schemas.user import UserRead, UserUpdate
from ..crud.user_db import get_user_by_id,reflush_user,get_user_by_email
from ..crud.token import encode_access_token,encode_refresh_token
from ..crud.base import verify_password

router = APIRouter()

@router.post(
"/Login_user",
# response_model = UserRead
)
async def login_user(
    userpassword: str,
    db: Annotated[AsyncSession , Depends(get_db)],
    userid: str = Query(default=None),
    # useremail: str = Query(default=None)
    ):
    
    """
        登录主接口：
        args:
        UserId: str
        UserPassword: str
        UserEmail: str

        应该返回tokens，refresh和Access Token ，还有User Info
    """

    if  not userid:
        raise HTTPException(400,"需要ID") 
    elif not userpassword:
        raise HTTPException(400,"需要密码")
    
    curr_user = await get_user_by_id(userid,db) 
    if verify_password(userpassword,curr_user.UserPassword):

        access_token = await encode_access_token(userid,db)
        refresh_token = await encode_refresh_token(userid,db)

    else:
        raise HTTPException(status_code=400, detail="密码错误")

    return{'access_token':access_token,'refresh_token':refresh_token}


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