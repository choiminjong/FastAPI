import time
import datetime

class dbUtils:

    def selectAll(self, session, query):
        result = session.execute(query).fetchall()
        return result

    def insertQuery(self,session,table,data):

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        keys = ['created_at', 'updated_at']
        vals = [timestamp, timestamp]
        for key, val in data:
            keys.append(key)
            vals.append(val)

        keys = ",".join(keys)
        vals = "'"+"','".join(vals)+"'"

        try:
            query = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, keys, vals)
            session.execute(query)
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.commit()
            session.close()

        return query