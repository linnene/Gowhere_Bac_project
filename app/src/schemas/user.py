from pydantic import BaseModel, model_validator
from .role import RoleType


class UserLogin(BaseModel):
    """
    UserLogin 是为了对登录时提交的表单的简化

    Example:{
            "UserId": 其实就是电话号码
            "UserEmail":  电子邮箱
            "UserPassword": 明文提交 
            P:注意，邮箱与ID至少有一个
    }
    """

    UserId:str
    UserEmail:str
    UserPassword:str

            
    @model_validator(mode='after')
    def check_id_or_email(self) -> 'UserLogin':

        if not self.UserId and not self.UserEmail:
            raise ValueError('UserId 和 UserEmail 至少需要提供一个')
        return self


class UserSignUp(BaseModel):
    """
    UserSignUp 是为了对注册时提交的表单的简化
    
    Example:{
            "UserId": 其实就是电话号码
            "UserEmail":  电子邮箱
            "UserPassword": 明文提交 
            P:注意，邮箱与ID至少有一个
    }  
    """

    UserId: str
    UserEmail: str

    UserPassword: str
    UserName: str
    


class UserCreate(UserSignUp):
    """
    UserCreate is a Pydantic model that is used to validate
    the data that is sent to the server when creating a new user.
    创建新用户使用的模型
    Example:
            {
                "UserId": "18085588360",
                "UserName": "Line",
                "UserPassword": "ioiz73763",
                "UserEmail": "1234@qq.com",
                UserEmailVerified: bool = False,
                "Is_Ban": false
            }   
    """

    #SAME AS PHONE NUMBER
    UserEmailVerified: bool = False
    
    Is_Ban: bool = False
    
    role: RoleType = RoleType.user

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    """
    UserRead is a Pydantic model that is used to validate
    the data that is sent to the server when reading a user.
    读取用户使用的模型
    """
    UserName: str
    UserEmail: str
    #SAME AS PHONE NUMBER
    UserId: str
    Is_Ban: bool 
    UserEmailVerified: bool = False
    
    class Config:
        from_attributes = True

    

class UserUpdate(BaseModel):
    """
    UserUpdate is a Pydantic model that is used to validate
    the data that is sent to the server when updating a user.
    更新用户使用的模型
    """
    
    UserName: str
    UserPassword: str
    UserEmail: str    
    Is_Ban: bool
    UserEmailVerified: bool = False

    class Config:
        from_attributes = True