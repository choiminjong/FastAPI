# 사용버전
- PyMySQL	1.0.2	
- SQLAlchemy	1.3.23
- click	7.1.2
- fastapi	0.63.0
- h11	0.12.0
- pip	21.0.1
- pydantic	1.8
- setuptools	53.1.0
- starlette	0.13.6
- typing-extensions	3.7.4.3
- uvicorn	0.13.4

# SQLAlchemy 세션을 이용해서 PURE query 실행 
- router index get/post 예시 생성 

# docs 섹터분리
- router = APIRouter( prefix="/items",tags=["items"] 등으로 docs 섹터분리)

# model 추가 
- client 데이터 받을때 모델 데이터 참조 

# confing (common 폴더) 
- config.py 파일안에 커넥션 정보 
- conn.py DB연결 

# main.py (include_router/DB conf)
- app.include_router(index.router)
- conf_dict = asdict(c) (from dataclasses import asdict 클래스를 딕셔너리 반환)

# FastAPI (참고 소스) 
- https://github.com/riseryan89/notification-api


databaseinit

