import time
import typing
import re
import jwt

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

#유틸
from app.utils.date_utils import dateUtils

#config
from app.common.consts import JWT_SECRET,JWT_ALGORITHM

#헤더 token 검색
class AccessControl:

    def __init__(self, app: ASGIApp, except_path_list: typing.Sequence[str] = None, except_path_regex: str = None, ) -> None:
        if except_path_list is None:
            except_path_list = ["*"]

        self.app = app
        self.except_path_list = except_path_list
        self.except_path_regex = except_path_regex

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope=scope)
        cookies = request.cookies

        request.state.req_time = dateUtils.datetime()
        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.is_admin_access = None

        if await urlPatternCheck(request.url.path, self.except_path_regex) or request.url.path in self.except_path_list:
            print("urlPatternCheck")
            return await self.app(scope, receive, send)
        
        #임시 테스트
        request.cookies["Authorization"] ="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoic3RyaW5nIiwiZW1haWwiOiJzdHJpbmciLCJwaG9uZV9udW1iZXIiOjAsInNuc190eXBlIjowfQ.CHVgE6Z7mhNKClNKGZBQUPqbuhk81SPNGc2f4z_SP9g"

        if "Authorization" not in cookies.keys():
            print("Not Authorization")

        token_info = await token_decode(access_token=cookies.get("Authorization"))

        res = await self.app(scope, receive, send)
        return res

async def urlPatternCheck(path, pattern):
    """
    :param path:
    :param pattern:
    :return:
    """

    result = re.match(pattern, path)
    if result:
        return True
    return False

async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """

    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.DecodeError:
        return 'Token is not valid.'
    except jwt.ExpiredSignatureError:
        return 'Token is expired.'
    return payload



