from pydantic import BaseModel
from enum import Enum

class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"

class UserRegister(BaseModel):
    name: str = None
    email: str = None
    pw: str = None
    phone_number: str = None
    sns_type: str = '1'
    marketing_agree: str = '1'


class Token(BaseModel):
    Authorization: str = None

class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True