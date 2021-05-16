## config
- consts.py : middlewares path  예외처리 / jwt 옵션 추가 
- environment.py : 모드에따라 커넥션 변경 가능 (ex)CONENCTION)

## middlewares
- access_control.py : 통신 전 검토단계 (로그인 여부 검토/URL 예외처리)

## atabases
- connector.py : 함수 => asdict(conf(CONFIGMOD) : CONFIGMOD(모드 변수 추가)

## router
- auth.py: 로그인/로그아웃/jwt 암복화 기본틀 제작

## utils
- logger.py : middlewares Request 체크 후 함수 => httplogger 로깅 처리 
- pemissoncheker.py : Decorator 방식으로 권한 체크 로직 추가할 예정 
- ex) async def custom_swagger_ui_html( pemisson : str = Depends(pemissoncheker("admin"))):