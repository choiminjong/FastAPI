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
from fastapi.security import APIKeyCookie

# [errors]
from app.errors import exceptions as ex

# [templates]
from fastapi.templating import Jinja2Templates

from app.utils.jwt import get_current_user,create_access_token,token_decode

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
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

templates = Jinja2Templates(directory="public")

@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if username not in users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN"
        )

    db_password = users[username]["password"]
    if not password == db_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN"
        )

    token =f"Authorization: Bearer {await create_access_token(username,password)}"
    response.set_cookie("Authorization", token)
    return True


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


