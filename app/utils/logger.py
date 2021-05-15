import os
import json

import logging
import logging.handlers

from time import time
from datetime import timedelta, datetime

from fastapi.requests import Request
from fastapi.logger import logger

# 현재 파일 경로 및 파일명 찾기
current_dir = os.path.dirname(os.path.realpath(__file__))
current_file = os.path.basename(__file__)
current_file_name = current_file[:-3]  # xxxx.py
LOG_FILENAME = current_dir+'/logs/log-{}'.format(current_file_name)

# 로그 저장할 폴더 생성
log_dir = '{}/logs'.format(current_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 로거 생성
logger = logging.getLogger('INFO') 
logger.setLevel(logging.INFO) 

# 핸들러 생성
file_handler = logging.handlers.TimedRotatingFileHandler(
  filename=LOG_FILENAME, when='midnight', interval=1,  encoding='utf-8') # 자정마다 한 번씩 로테이션
file_handler.suffix = 'log-%Y%m%d' # 로그 파일명 날짜 기록 부분 포맷 지정 

logger.addHandler(file_handler) # 로거에 핸들러 추가
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')
file_handler.setFormatter(formatter) # 핸들러에 로깅 포맷 할당

async def httplogger(request: Request, response=None, error=None):

    time_format = "%Y/%m/%d %H:%M:%S"
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    user = request.state.user
    body = await request.body()
    if error:
        if request.state.inspect:
            frame = request.state.inspect
            error_file = frame.f_code.co_filename
            error_func = frame.f_code.co_name
            error_line = frame.f_lineno
        else:
            error_func = error_file = error_line = "UNKNOWN"

        error_log = dict(
            errorFunc=error_func,
            location="{} line in {}".format(str(error_line), error_file),
            raised=str(error.__class__.__name__),
            msg=str(error.ex),
        )

    email = user.email.split("@") if user and user.email else None
    user_log = dict(
        client=request.state.ip,
        user=user.id if user and user.id else None,
        email="**" + email[0][2:-1] + "*@" + email[1] if user and user.email else None,
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_log,
        client=user_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeUTC=datetime.utcnow().strftime(time_format),
        datetimeKR=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format),
    )
    if body:
        log_dict["body"] = body
    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))
