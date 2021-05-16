#config
- consts.py : middlware path  예외처리 / jwt 옵션 추가 
- environment.py : 모드에따라 커넥션 변경 가능 (ex)CONENCTION)

#middlewares
- access_control.py : 통신전 검토단계 (ex)로그인 여부 검토/URL 예외처리)

#databases
- connector.py : 함수 =>asdict(conf(CONFIGMOD) : CONFIGMOD(모드 변수추가)

#router
- auth.py: 로그인/로그아웃/jwt 암복화 기본틀 작업

#utils
- logger.py : middlware에서 데이터 체크 후 httplogger 함수에서 가공처리
- pemissoncheker.py : 데코레이터으로 권한 체크 class 추가할 예정 
- ex) async def custom_swagger_ui_html( pemisson : str = Depends(pemissoncheker("admin"))):
