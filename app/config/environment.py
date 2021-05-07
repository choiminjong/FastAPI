from dataclasses import dataclass
from os import path, environ
from typing import List

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir


@dataclass
class TestConfig(Config):
    CONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"
    CONFDEVCONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"

@dataclass
class LocalConfig(Config):
    CONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"
    CONFDEVCONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"

@dataclass
class ProdConfig(Config):
    CONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"
    CONFDEVCONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"


@dataclass
class ConflLiveConfig(Config):
    CONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"
    CONFDEVCONENCTION : str = "HOST=127.0.0.1;USER=root;PWD=Vlvkahqkdlf#elvmf(3;DB=notification_api;CHARSET=utf8mb4"


def conf(mod):
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig,conflLive=ConflLiveConfig)
    return config[mod]()
