import psycopg2
import json
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)


class BaseWrapper:
    def __init__(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        bd_data = data["postgres"]
        # try:
        self.conn = psycopg2.connect(database=bd_data["db"], user=bd_data["user"],
                                     host=bd_data["host"], password=bd_data["password"])
        # except:
        #     self.conn = None
        #     logging.error("Unable to connect to the database. Please, check")
        #     raise
