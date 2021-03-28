from datetime import datetime, date, timedelta

class dateUtils:
    def __init__(self, *args):
        self.utc_now = datetime.utcnow()
        self.timedelta = 0

    @classmethod
    def datetime(cls, diff: int=0) -> datetime:
        """
        :return: 2021-03-28 08:28:41.899126
        """
        return cls().utc_now + timedelta(hours=diff) if diff > 0 else cls().utc_now + timedelta(hours=diff)

    @classmethod
    def date(cls, diff: int=0) -> date:
        """
        :return: 2021-03-28
        """
        return cls.datetime(diff=diff).date()

    @classmethod
    def date_num(cls, diff: int=0) -> int:
        """
        :return: 20210328
        """
        return int(cls.date(diff=diff).strftime('%Y%m%d'))