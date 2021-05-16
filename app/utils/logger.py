import os
import json

import logging
import logging.handlers

from time import time
from datetime import timedelta, datetime

from fastapi.requests import Request
from fastapi.logger import logger


# [logging path/filename]
current_dir = os.path.dirname(os.path.realpath(__file__))
current_file = os.path.basename(__file__)
current_file_name = current_file[:-3]  # xxxx.py
LOG_FILENAME = current_dir+'/logs/log-{}'.format(current_file_name)

# [logging folder make]
log_dir = '{}/logs'.format(current_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# [logging level]
logger = logging.getLogger('INFO') 
logger.setLevel(logging.INFO) 

# [logging handler]
file_handler = logging.handlers.TimedRotatingFileHandler(
filename=LOG_FILENAME, when='midnight', interval=1,  encoding='utf-8') 
file_handler.suffix = 'log-%Y%m%d' 

logger.addHandler(file_handler) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')
file_handler.setFormatter(formatter) 

async def httplogger(request: Request, response=None, error=None):

    time_format = "%Y/%m/%d %H:%M:%S"
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    user = request.state.user

    email = user.email.split("@") if user and user.email else None
    user_log = dict(
        client=request.state.ip,
        user=user.id if user and user.id else None,
        email="**" + email[0][2:-1] + "*@" + email[1] if user and user.email else None,
    )

    #[Log format]
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

    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))

