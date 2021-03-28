from datetime import datetime, timedelta

import time
import datetime

#token
import bcrypt
import jwt
from app.common.consts import JWT_SECRET, JWT_ALGORITHM

#TODO
from fastapi import APIRouter
from starlette.responses import JSONResponse

#DB
from app.database.DBConnector import DBConnector

#모델
from app.model.auth import UserRegister,Token

'''
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method not allowed
500 Internal Error
502 Bad Gateway 
504 Timeout
200 OK
201 Created
'''

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
    responses={404: {"description": "Not found"}},
)

@router.post("/",status_code=201, response_model=Token)
async def register(UserRegister: UserRegister):
    """
    `회원가입 API`\n
    :param UserRegister:
    :return: Token
    """
    is_exist = await isEmailExist(UserRegister.email)
    if not UserRegister.email or not UserRegister.pw:
        return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))

    # 계정생성
    UserRegister.pw = bcrypt.hashpw(UserRegister.pw.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    executedata = {'status': 'active', 'created_at': timestamp, 'updated_at': timestamp}
    executedata.update(dict(UserRegister))
    DBConnector().execute(DBConnector().insertQuery('users', executedata))

    #토큰발행
    token = dict(Authorization=f"Bearer {createAccessToken(data=UserRegister.dict(exclude={'pw', 'marketing_agree'}),)}")
    return token


@router.post("/login/", status_code=200, response_model=Token)
async def login(UserRegister: UserRegister):
    """
    `로그인 API`\n
    :param UserRegister:
    :return: Token
    """
    is_exist = await isEmailExist(UserRegister.email)
    if not UserRegister.email or not UserRegister.pw:
        return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
    if not is_exist:
        return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))

    user = await pwValid(UserRegister.email)
    isVerified = bcrypt.checkpw(UserRegister.pw.encode('utf-8'), user['pw'].encode('utf-8'))

    if not isVerified:
         return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))

    #토큰발행
    token = dict(Authorization=f"Bearer {createAccessToken(data=UserRegister.dict(exclude={'pw', 'marketing_agree'}),)}")
    return token

async def isEmailExist(email: str):
    query = "SELECT * FROM users where email='" + email + "'"
    get_email = DBConnector().fetchone(query)
    if get_email:
        return True
    return False

async def pwValid(email: str):
    query = "SELECT * FROM users where email='" + email + "'"
    get_pw = DBConnector().fetchone(query)
    return get_pw

def createAccessToken(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt