from fastapi import APIRouter
from starlette.responses import Response
from app.database.connector import DBConnector

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/fetchone")
async def fetchone():
    data = {'no': '1', 'age': 74}
    query = "select * from users where no = {no}".format(no=data['no'], age=data['age'])
    result =  DBConnector('CONENCTION').select(query)
    return result


@router.get("/fetchall")
async def fetchall():
    query = "select * from users "
    result =  DBConnector('CONENCTION').select(query)
    return result

@router.get("/insert")
async def insert():
    data = {'status': 'actic', 'name': '세종대왕','phone_number': '0100000','sns_type': '22'}
    result =  DBConnector('CONENCTION').insert('users', status=data['status'], name=data['name'], phone_number=data['phone_number'], sns_type=data['sns_type'])
    
    return result

@router.get("/update/{cno}")
async def updata(cno : int):
    conditional_query = "no = {no}".format(no=cno)
    result =  DBConnector('CONENCTION').update('users', conditional_query, name='dominic', phone_number='1111')

    return result
