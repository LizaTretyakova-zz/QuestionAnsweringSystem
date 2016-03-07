#!/usr/bin/env python3

from collections import namedtuple
from enum import Enum
import sys

Question = namedtuple("Question", ["question", "question_type", "answer_type", "attributes"])

class AnswerType(Enum):
    NUMBER = 0
    DATE = 1

class QuestionType(Enum):
    DOWNLOADS = 0
    MONEY = 1
    EVENTS = 2

ATTRIBUTES = {
    "country": ["Russia", "Japan", "Germany"],
    "product": ["PyCharm", "AppCode", "RubyMine", "ReSharper", "IntellijIdea"]
}

TYPES = {
    "interrogative": {
        "How many": AnswerType.NUMBER,
        "How much": AnswerType.NUMBER,
        "What": AnswerType.NUMBER,
        "When": AnswerType.DATE
    },

    "help_words": {
        "download": QuestionType.DOWNLOADS,
        "customer": QuestionType.MONEY,
        "revenue": QuestionType.MONEY,
        "release": QuestionType.EVENTS,
    }
}

def get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type

def get_attribute(attr_list, question):
    for word in attr_list:
        if word in question:
            return word

def process_qiestion(question):
    question_type = get_type("help_words", question)
    answer_type = get_type("interrogative", question)
    attributes = {}
    for attr, attr_list in ATTRIBUTES.items():
        attributes[attr] = get_attribute(attr_list, question)
    return Question(question=question, question_type=question_type, answer_type=answer_type, attributes=attributes)

def main():
    processed_question = process_qiestion(sys.argv[1])
    print(processed_question)
    if processed_question.question_type == None or processed_question.answer_type == None:
        print("Sorry, the question is not clear enough. Would you mind repeating it, please?")


main()
