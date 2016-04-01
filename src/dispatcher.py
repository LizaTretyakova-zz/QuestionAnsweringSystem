#!/usr/bin/env python3

from model import AnswerType, QuestionType
from attributes import TYPES
from database_wrappers import DownloadsWrapper


def dispatch(question):
    if question.question_type is None or question.answer_type == None:
        print("Sorry, the question is not clear enough. Would you mind repeating it, please?")
    else:
        print(question)
        return get_answer(question)


def get_answer(question):
    if question.question_type == QuestionType.DOWNLOADS:
        return DownloadsWrapper(question).get()


#deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type

