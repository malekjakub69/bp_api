import decimal
import json

import psycopg2.extras


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(database="scout_app", user='postgres', password='admin123', host='127.0.0.1', port='5432')
        # Creating a cursor object using the cursor() method
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def __del__(self):
        self.conn.close()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
