import uvicorn
from fastapi import FastAPI, Request
#router 
from app.router import index,page
#middleware 
from fastapi.middleware.cors import CORSMiddleware
#static
from fastapi.staticfiles import StaticFiles
#swagger
from fastapi.openapi.docs import (get_redoc_html,get_swagger_ui_html,get_swagger_ui_oauth2_redirect_html,)
#templates
from fastapi.templating import Jinja2Templates

def include_router(app) :
   app.include_router(index.router)
   app.include_router(page.router)

def configure_static(app) :  
    app.mount("/public", StaticFiles(directory="public"), name="public")

def configure_middleware(app) :  
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_app() :
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
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

    configure_middleware(app)
    include_router(app)
    configure_static(app) 

    return app

app = create_app()