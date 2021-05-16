# [fastapi]
from fastapi import APIRouter,FastAPI, Form, HTTPException, Depends, Request, Header
from fastapi.security import APIKeyCookie
from starlette import status
from starlette.responses import Response, HTMLResponse

# [jwt]
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from datetime import datetime, timedelta
from app.config.consts import JWT_SECRET,JWT_ALGORITHM

# [errors]
from app.errors import exceptions as ex

API_KEY_HEADER = APIKeyCookie(name="Authorization", auto_error=False)
secret_key = "someactualsecret"


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.get("/login")
async def login_page():
    return HTMLResponse(
        """
        <form action="/auth/login" method="post">
        Username: <input type="text" value="1" name="username" required>
        <br>
        Password: <input type="password" value="1" name="password" required>
        <input type="submit" value="Login">
        </form>
        """
    )

#임시 DB데이터 
users = {
        "1":{
            "password": "1",
            "data": "1"
        },
        "tiangolo":{
            "password": "secret2"
        }
}

@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if username not in users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
        )

    db_password = users[username]["password"]
    if not password == db_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
        )

    token =f"Authorization: Bearer {await create_access_token(username,password)}"
    response.set_cookie("Authorization", token)
    return token

async def get_current_user(request: Request):
    try:
        cookie_authorization: str = request.cookies.get("Authorization")
        payload=await token_decode(cookie_authorization)
        return payload   
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
        )

@router.get("/private")
async def read_private(request: Request, username: str = Depends(get_current_user)):
    """
    jwt.decode data return:
    """    
    return {"username": username, "private": "get some private data"}

@router.get("/logout")
async def logout(response: Response):
    """
    delete_cookie return:
    """       
    response.delete_cookie("Authorization")
    return {"ok": True}

async def create_access_token(username, password, expires_delta: int = None):
    """
    :param username / password :
    :return:
    """      
    to_encode= {"username": username,"password": password}
    
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Authorization: Bearer ", "")
        payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()