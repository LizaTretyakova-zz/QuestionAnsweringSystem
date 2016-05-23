import psycopg2


class BaseWrapper:
    def __init__(self):
        import sys
        from os.path import dirname, abspath

        sys.path.insert(0, dirname(dirname(abspath(__file__))))
        import config

        bd_data = config.get_db_data()
        self.conn = psycopg2.connect(database=bd_data["db"], user=bd_data["user"],
                                     host=bd_data["host"], password=bd_data["password"])
