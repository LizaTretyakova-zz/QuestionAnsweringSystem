#!/usr/bin/env python3

from enum import Enum
from model import Question
import psycopg2

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


def dispatch(question):
    question = question._replace(question_type=get_question_type(question.question))
    question = question._replace(answer_type=get_answer_type(question.question))
    if question.question_type is None or question.answer_type == None:
        print("Sorry, the question is not clear enough. Would you mind repeating it, please?")
    else:
        print(question)
        return get_answer(question)


def get_answer(question):
    conn = psycopg2.connect(database="postgres", user="qa", password="ulizoturome", host="localhost")
    cur = conn.cursor()
    query = ""
    if question.question_type == QuestionType.DOWNLOADS:
        query = "select sum(amount) from downloads where lower(country) = coalesce(lower(%s), lower(country))"
    print(query, (question.attributes["country"],))
    cur.execute(query, (question.attributes["country"],))
    return cur.fetchall()



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