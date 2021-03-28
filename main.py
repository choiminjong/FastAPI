import uvicorn
from fastapi import FastAPI

#라우터
from app.router import auth, index

#미들웨어
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.middlewares.token_validator import AccessControl

#CORS
from starlette.middleware.cors import CORSMiddleware

#config
from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX,LocalConfig


def create_app() :

    app = FastAPI()

    # 미들웨어 정의
    app.add_middleware(AccessControl, except_path_list=EXCEPT_PATH_LIST, except_path_regex=EXCEPT_PATH_REGEX)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=LocalConfig.ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=LocalConfig.TRUSTED_HOSTS)

    # router
    app.include_router(index.router)
    app.include_router(auth.router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)