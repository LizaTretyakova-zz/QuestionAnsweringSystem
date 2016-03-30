#!/usr/bin/env python3

from attributes import AnswerType, QuestionType, TYPES
from database_wrappers import get_from_downloads


def dispatch(question):
    if question.question_type is None or question.answer_type == None:
        print("Sorry, the question is not clear enough. Would you mind repeating it, please?")
    else:
        print(question)
        return get_answer(question)


def get_answer(question):
    if question.question_type == QuestionType.DOWNLOADS:
        return get_from_downloads(question)


#deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type
