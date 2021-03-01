import json

class dbUtils:

    def selectAll(self, session, query):
        result = session.execute(query).fetchall()
        return result


