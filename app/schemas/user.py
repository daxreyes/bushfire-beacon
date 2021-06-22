from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic import validator
from uuid import UUID

# from fastapi_users import models


# class User(models.BaseUser):
#     pass


# class UserCreate(models.BaseUserCreate):
#     @validator('password')
#     def valid_password(cls, v: str):
#         if len(v) < 8:
#             raise ValueError('Password should be at least 8 characters')
#         return v


# class UserUpdate(User, models.BaseUserUpdate):
#     pass


# class UserDB(User, models.BaseUserDB):
#     pass


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_verified: bool = False
    is_superuser: bool = False
    is_volunter: bool = False
    is_hospital_staff: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
