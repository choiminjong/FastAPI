#권한관리 체크
class pemissoncheker:
    def __init__(self, auth: str):
        self.auth = auth

    def __call__(self):
        print(self.auth)