#!/usr/bin/env python3
import itertools

from answer_maker import get_answer
from model import QuestionType
from database_wrappers import WrapperMoneyDatabase, DownloadsWrapper


def itertools_to_list(iter):
    return [item for item in iter]

databases_ask_functions = {
    WrapperMoneyDatabase.ask
}


class Dispatcher(object):
    @staticmethod
    def find_answer(meta_data):
        meta_data.attributes.print()
        if meta_data.question_type is QuestionType.MONEY:
            return WrapperMoneyDatabase.ask(meta_data)
        if meta_data.question_type is QuestionType.DOWNLOADS:
            wrapper = DownloadsWrapper(meta_data)
            downloads_answer = wrapper.get()
            if downloads_answer['message'] is "Success":
                return  downloads_answer["result"]
            else:
                print(downloads_answer["message"])
