import time
from starlette.requests import Request
from app.utils.date_utils import D
from app.utils.logger import httplogger


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

    response = await call_next(request)
    await httplogger(request=request, response=response)
    
    return response