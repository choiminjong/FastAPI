from enum import Enum
from pydantic import BaseModel

class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"

class UserRegister(BaseModel):
    name: str  = None
    email: str  = None
    pw: str = None
    phone_number: int
    sns_type: int
    marketing_agree: int

class id(BaseModel):
    id: str = ""

class Token(BaseModel):
    Authorization: str = ""

class UserToken(BaseModel):
    id: int
    email: str = ""
    name: str = ""
    phone_number: str = ""
    profile_img: str = ""
    sns_type: str = ""