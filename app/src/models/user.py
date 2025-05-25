from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import mapped_column, Mapped
from typing import Text

from .base import Base
from ..schemas.role import RoleType

class User(Base):
    """
    TODO: 
        完善User表项
    """
    __tablename__ = "user"

    UserId: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, index=True)
    UserEmail: Mapped[str] = mapped_column(String(255), index=True)

    # hashed_password
    UserPassword: Mapped[str] = mapped_column(String(255), index=False)
    UserName: Mapped[str] = mapped_column(String(255), index=True)  

    # is email verified
    UserEmailVerified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    #Ai Chat 
    ChatHistory = mapped_column(Text,default=None)#type:ignore

    # is BAN
    Is_Ban: Mapped[bool] = mapped_column(Boolean, default=True)

    role: Mapped[RoleType] = mapped_column(
        Enum(RoleType),
        nullable=False,
        server_default=RoleType.user.name,
        index=True,
    )