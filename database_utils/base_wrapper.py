import psycopg2


USER = "demo"
PASSWORD = "demo"


class BaseWrapper:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(database='postgres', user=USER, host='localhost', password=PASSWORD)
        except:
            self.conn = None
            print("Unable to connect to the database")
        # pass