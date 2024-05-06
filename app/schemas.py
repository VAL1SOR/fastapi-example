from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
  title: str = None
  content: str = None

class PostCreate(PostBase):
  owner_id: Optional[int] = None

class UpdatePost(PostBase):
  pass

class UserOut(BaseModel):
  id: int
  username: str
  email: EmailStr
  time: datetime

  class Config:
    from_attributes = True

class Post(PostBase):
  time: datetime
  id: int
  owner: UserOut

  class Config:
    from_attributes = True

class UserCreate(BaseModel):
  username: str = "user"
  email: EmailStr = None
  password: str = None

class UserLogin(BaseModel):
  email: EmailStr = None
  password: str = None

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int
  username: str

class Vote(BaseModel):
  post_id: int

class PostOut(BaseModel):
  Post: Post
  votes: int

  class Config:
    from_attributes = True