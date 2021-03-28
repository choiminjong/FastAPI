# 사용버전
- PyJWT	2.0.1	2.0.1
- PyMySQL	1.0.2	1.0.2
- bcrypt	3.2.0	3.2.0
- cffi	1.14.5	1.14.5
- click	7.1.2	7.1.2
- cryptography	3.4.7	3.4.7
- fastapi	0.63.0	0.63.0
- h11	0.12.0	0.12.0
- jwt	1.2.0	1.2.0
- pip	21.0.1	21.0.1
- pycparser	2.20	2.20
- pydantic	1.8.1	1.8.1
- setuptools	54.2.0	54.2.0
- six	1.15.0	1.15.0
- starlette	0.13.6	0.14.2
- typing-extensions	3.7.4.3	3.7.4.3
- urlparser	0.1.2	0.1.2
- uvicorn	0.13.4	0.13.4

# pymysql class 생성  
- fetchall (O)
- fetchone (O)
- insertQuery (O)
- updateQuery (X)
- execute (O)

# common 폴더
- consts.py config 데이터 모음 

# main.py
- app.include_router 라우터 설정 
- app.add_middleware CORS/ Middleware AccessControl 설정 (except_path_list/EXCEPT_PATH_REGEX) 

# utils 폴더 
- data 날짜 포맷 클래스 (2021-03-28 08:28:41.899126/2021-03-28/20210328)

# JWT 토근 발행
- Router/auth/register 회원가입 후 토큰 발행 
- Router/auth/register 로그인 후 토큰 발행
- JWT 기본틀만 검토 만료시간없음 

# 인증 
- bcrypt 패스워드 .decode('utf-8') 후 .encode('utf-8')으로 패스워드 검토 
- bcrypt.checkpw(UserRegister.pw.encode('utf-8'), user['pw'].encode('utf-8')) 
- 참고 str -> byte 검증 
 
# FastAPI (참고 소스) 
- https://github.com/riseryan89/notification-api

