from fastapi import APIRouter,Request, Depends ,Form
from fastapi.responses import HTMLResponse

from starlette.responses import Response
from app.database.connector import DBConnector
from fastapi.templating import Jinja2Templates

# [pemissoncheker]
from app.utils.pemissoncheker import pemissoncheker

router = APIRouter(
    prefix="/page",
    tags=["page"],
    responses={404: {"description": "Not found"}},
)


