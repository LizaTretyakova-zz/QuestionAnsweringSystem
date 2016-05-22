import logging.config
import logging
import json

import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))


def get_config_data() -> dict:
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data


def get_logger() -> logging.Logger:
    data = get_config_data()
    logging.config.dictConfig(data["logging"])
    logger = logging.getLogger(__name__)
    return logger


def get_bd_data() -> dict:
    data = get_config_data()
    bd_data = data["postgres"]
    return bd_data


if __name__ == '__main__':
    get_logger()