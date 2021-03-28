from fastapi import APIRouter, Depends
from starlette.responses import Response

#DB
from app.database.DBConnector import DBConnector

#모델
from app.model.index import Project
from datetime import datetime

#모델
from app.model.auth import UserRegister

import time
import datetime

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


'''
@router.get("/{item_id}")
async def read_item():
    query = 'SELECT * FROM users'
    return DBConnector().fetchall(query)
'''

@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.get("/id/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/id2/")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/",status_code=201)
async def register(UserRegister: UserRegister):
    Register = {'name': UserRegister.name }
    print(DBConnector().insertQuery('users', Register))
    return UserRegister

@router.post("/2",status_code=201)
async def register(UserRegister: UserRegister):
    Register = {'name': UserRegister.name }
    condition = {'no': UserRegister.no}
    print(DBConnector().updateQuery('users', Register, condition))
    return UserRegister

@router.post("/3",status_code=201)
async def register(UserRegister: UserRegister):
    condition = {'no': 1 , 'name' : 'dominic'}
    #condition = {'no': 1}
    print(DBConnector().updateQuery('users', UserRegister,condition))
    return UserRegister
