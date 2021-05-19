
# [fastapi]
from fastapi import HTTPException, Request
from starlette import status
from starlette.responses import RedirectResponse, Response, HTMLResponse

# [jwt]
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from datetime import datetime, timedelta
from app.config.consts import JWT_SECRET,JWT_ALGORITHM

# [errors]
from app.errors import exceptions as ex
# [templates]
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="public")

async def get_current_user(request: Request):
    try:
        cookie_authorization: str = request.cookies.get("Authorization")
        payload=await token_decode(cookie_authorization)
        return payload   
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN22"
        )

async def create_access_token(username, password, expires_delta: int = None):
    """
    :param username / password :
    :return:
    """    
    try :  
        to_encode= {"username": username,"password": password}
        
        if expires_delta:
            to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return encoded_jwt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN"
        )

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