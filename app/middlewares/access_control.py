import time

# [fastapi]
from fastapi import Request,HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse,RedirectResponse

# [utils/config]
from app.utils.date_utils import D
from app.utils.logger import httplogger
from datetime import datetime, timedelta
from app.config.consts import EXCEPT_PATH_LIST,lOGINURL

# [errors]
from app.errors import exceptions as ex
from app.errors.exceptions import APIException

# [templates]
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# [JWT]
from app.utils.jwt import token_decode

async def access_control(request: Request, call_next):
    
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip

    headers = request.headers
    cookies = request.cookies
    url = request.url.path

    if url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        return response

    try:
        if "Authorization" not in cookies.keys():   
            return RedirectResponse(
                url=lOGINURL,
                status_code=302,
            )  

        response = await call_next(request)

    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await httplogger(request=request, error=error)

    return response

async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
