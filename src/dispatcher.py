#!/usr/bin/env python3
import psycopg2
from src.answer_maker import get_answer
from src.model import QuestionType
import database_utils

import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import config
logger = config.get_logger()


def itertools_to_list(iter):
    return [item for item in iter]


databases_ask_functions = {
    database_utils.CustomersWrapper.ask
}


class Dispatcher(object):
    @staticmethod
    def find_answer(meta_data):
        # import sys
        # from os.path import dirname, abspath
        #
        # sys.path.insert(0, dirname(dirname(abspath(__file__))))
        # import config
        #
        # logger = config.get_logger()

        if meta_data is None:
            return None
        logger.debug(meta_data.attributes)
        try:
            if meta_data.question_type is QuestionType.CUSTOMERS:
                wrapper = database_utils.CustomersWrapper()
                return get_answer(meta_data, wrapper.ask(meta_data))
            if meta_data.question_type is QuestionType.DOWNLOADS:
                wrapper = database_utils.DownloadsWrapper()
                downloads_answer = wrapper.get(meta_data)
                if downloads_answer['message'] is "Success":
                    return get_answer(meta_data, downloads_answer["result"][0])
                else:
                    return (get_answer(meta_data, 0) + "\n" +
                            downloads_answer["message"])
        except KeyError as e:
            logger.error("KeyError. Json config doesn't contain such key:", str(e))
            raise e
        except psycopg2.OperationalError as e:
            logger.error("Error during database operation:\n", str(e))
            raise e
