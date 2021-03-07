from datetime import datetime, timedelta

#token
import bcrypt
import jwt
from app.common.consts import JWT_SECRET, JWT_ALGORITHM

#TODO
from fastapi import APIRouter, Depends
from starlette.responses import Response
from starlette.responses import JSONResponse

#DB
from app.database.conn import db
from sqlalchemy.orm import Session
from app.database.pymysql import dbUtils

#모델
from app.model.auth import SnsType,UserRegister,Token,UserToken

from collections import defaultdict

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
    prefix="/register",
    tags=["Authorization"],
    responses={404: {"description": "Not found"}},
)

@router.post("/",status_code=201)
async def register(UserRegister: UserRegister, session: Session = Depends(db.session)):
    sql = dbUtils().insertQuery(session, 'users', UserRegister)

    return sql

'''
@router.post("/{sns_type}",status_code=201, response_model=Token)
async def register(sns_type: SnsType, reg_info: UserRegister, session: Session = Depends(db.session)):

    #query = 'SELECT * FROM users WHERE no = :no', {'no': item_id}
    #query = 'SELECT * FROM users WHERE no = '+SnsType
    #query = 'SELECT * FROM users '
    #dbUtils().selectAll(session, query)

    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())
    sql = 'INSERT INTO `test_gevent` (`ip`, `port`, `types`, `score`, `updatetime`) VALUES ("{}", "{}", "{}", "{}", "{}")'.format(
        data['ip'],
        data['port'],
        data['types'],
        DEFAULT_SCORE,
        datetime.datetime.utcnow(),
    )

    return True
'''