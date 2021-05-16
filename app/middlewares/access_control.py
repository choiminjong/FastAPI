
import re
import jwt
import time

# [fastapi]
from fastapi import Request
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.responses import Response, HTMLResponse

# [utils/config]
from app.utils.date_utils import D
from app.utils.logger import httplogger
from datetime import datetime, timedelta
from app.config.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX

# [errors]
from app.errors import exceptions as ex
from app.errors.exceptions import APIException

async def access_control(request: Request, call_next):

    # [Next Action Class checker]
    #response = await call_next(request)
    # [httplogger format ]
    #await httplogger(request=request, response=response)

    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip

    headers = request.headers
    cookies = request.cookies

    url = request.url.path
    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        return response

    try:
        if url.startswith("/api"):
            pass   
        else :
            if "Authorization" not in cookies.keys():
                raise ex.NotAuthorized()
                
        response = await call_next(request)

    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await httplogger(request=request, error=error)

    return response

async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
