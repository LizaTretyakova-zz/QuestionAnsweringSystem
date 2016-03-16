#!/usr/bin/env python3

from enum import Enum

class AnswerType(Enum):
    NUMBER = 0
    DATE = 1


class QuestionType(Enum):
    DOWNLOADS = 0
    MONEY = 1
    EVENTS = 2


TYPES = {
    "interrogative": {
        "how many": AnswerType.NUMBER,
        "how much": AnswerType.NUMBER,
        "what": AnswerType.NUMBER,
        "when": AnswerType.DATE
    },

    "help_words": {
        "download": QuestionType.DOWNLOADS,
        "customer": QuestionType.MONEY,
        "revenue": QuestionType.MONEY,
        "release": QuestionType.EVENTS,
    }
}

#deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type


def get_question_type(question):
    for word, q_type in TYPES["help_words"].items():
        if word in question:
            return q_type


def get_answer_type(question):
    for word, ans_type in TYPES["interrogative"].items():
        if word in question:
            return ans_type