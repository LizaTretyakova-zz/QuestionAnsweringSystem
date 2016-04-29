#!/usr/bin/env python3

from src.answer_maker import get_answer
from src.customers_wrapper import CustomersWrapper
from src.downloads_wrapper import DownloadsWrapper
from src.model import QuestionType


def itertools_to_list(iter):
    return [item for item in iter]


databases_ask_functions = {
    CustomersWrapper.ask
}


class Dispatcher(object):
    @staticmethod
    def find_answer(meta_data):
        if meta_data is None:
            return None
        print(meta_data.attributes)
        if meta_data.question_type is QuestionType.CUSTOMERS:
            wrapper = CustomersWrapper()
            return get_answer(meta_data, wrapper.ask(meta_data))
        if meta_data.question_type is QuestionType.DOWNLOADS:
            wrapper = DownloadsWrapper(meta_data)
            downloads_answer = wrapper.get()
            if downloads_answer['message'] is "Success":
                return get_answer(meta_data, downloads_answer["result"][0])
            else:
                return (get_answer(meta_data, 0) + "\n" +
                        downloads_answer["message"])
