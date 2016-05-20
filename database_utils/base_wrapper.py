import psycopg2
import json


class BaseWrapper:
    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        bd_data = data["postgres"]
        try:
            self.conn = psycopg2.connect(database=bd_data["db"], user=bd_data["user"],
                                         host=bd_data["host"], password=bd_data["password"])
        except:
            self.conn = None
            print("Unable to connect to the database")
            raise
