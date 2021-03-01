from fastapi import APIRouter, Depends
from starlette.responses import Response

#DB
from sqlalchemy.orm import Session
from app.database.conn import db
from app.database.pymysql import dbUtils

#모델
from app.model.index import Project
from datetime import datetime

'''
참고
https://fastapi.tiangolo.com/tutorial/bigger-applications/
'''
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_id}")
async def read_item(item_id:str, session: Session = Depends(db.session)):
    #query = 'SELECT * FROM users WHERE no = :no', {'no': item_id}
    query = 'SELECT * FROM users WHERE no = '+item_id
    #query = 'SELECT * FROM users '
    return dbUtils().selectAll(session, query)

@router.post("/project")
async def read_item(Project: Project, session: Session = Depends(db.session)):
    #print(Project)
    return Project

