import uvicorn
# [fastapi/static Path/swagger]
from fastapi import FastAPI, Form, HTTPException, Depends, Request, Header
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (get_redoc_html,get_swagger_ui_html,get_swagger_ui_oauth2_redirect_html,)

# [middleware]
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.access_control import access_control


# [starlette]
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

# [templates]
from fastapi.templating import Jinja2Templates

# [router] 
from app.router import index,page,auth
from app.utils.pemissoncheker import pemissoncheker
from app.errors import exceptions as ex

def include_router(app) :
   app.include_router(index.router)
   app.include_router(page.router)
   app.include_router(auth.router)

def configure_static(app) :  
    app.mount("/public", StaticFiles(directory="public"), name="public")

def configure_middleware(app) :  
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_app() :

    app = FastAPI(docs_url=None, redoc_url=None)

    configure_middleware(app)
    configure_static(app) 
    include_router(app)

    templates = Jinja2Templates(directory="public")

    @app.get("/", response_class=HTMLResponse)
    async def login(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    '''
    권한체크 
    pemisson : str = Depends(pemissoncheker("admin"))
    '''

    @app.get("/docs", include_in_schema=False )
    async def custom_swagger_ui_html( pemisson : str = Depends(pemissoncheker("admin"))):
        return get_swagger_ui_html(openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/public/static/swagger/swagger-ui-bundle.js",
            swagger_css_url="/public/static/swagger/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(openapi_url=app.openapi_url,title=app.title + " - ReDoc",redoc_js_url="/public/static/swagger/redoc.standalone.js",)   

    return app

app = create_app()