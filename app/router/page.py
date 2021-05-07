from fastapi import APIRouter,Request
from starlette.responses import Response
from app.database.connector import DBConnector
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/page",
    tags=["page"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="public")

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": "1"})
