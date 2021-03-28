
class Mysql() :
    HOST = "127.0.0.1"
    USER = "root"
    #PASSWORD = "Vlvkahqkdlf#elvmf(3"
    PASSWORD = "root"
    DATABASES = "notification_api"
    CHARSET = "utf8mb4"

class LocalConfig():
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]

JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/auth)"