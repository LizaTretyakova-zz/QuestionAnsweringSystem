import logging
import json

import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))


BOT = "bot"
LOGGER = "logging"
DB_DATA = "postgres"
FILENAME = "../config.json"

with open(FILENAME) as json_data_file:
    data = json.load(json_data_file)

logging.basicConfig(filename="qa.log", format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level="DEBUG")
print("logger name=" + __name__)
logger = logging.getLogger(__name__)


def get_config_data() -> dict:
    return data


def get_logger() -> logging.Logger:
    # logging.config.dictConfig(data[LOGGER])
    return logger


def get_db_data() -> dict:
    # data = get_config_data()
    bd_data = data[DB_DATA]
    return bd_data


def get_bot_data() -> dict:
    # data = get_config_data()
    bot_data = data[BOT]
    return bot_data


def update(field: str, value) -> None:
    data[field] = value
    get_logger().debug("New field %s in data %s", field, data)
    with open(FILENAME, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    get_logger()
