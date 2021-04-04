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


@router.post("/user/login", status_code=200)
async def userLogin(UserRegister: UserRegister):
    """
    `로그인 API`\n
    :return: Token
    :param UserRegister:
    참고 : https://velog.io/@inyong_pang/Flask-%EC%9D%B8%EC%A6%9D-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0
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

    token = dict(Authorization=f"Bearer {createAccessToken2(UserRegister)}")

    return token


@router.get("/vaild/{Token}" , status_code=200)
async def vaildToken(Token: str):
    return vailidToken(Token)

@router.post("/login/", status_code=200, response_model=Token)
async def login(UserRegister: UserRegister):
    """
    `로그인 API`\n
    :return: Token
    :param UserRegister:
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

def createAccessToken2(data):
    payload = {
        'userEmail': data.email,
        'exp': datetime.datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return encoded_jwt

def vailidToken(token):
    access_token = token.replace("Bearer ", "")
    payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload


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