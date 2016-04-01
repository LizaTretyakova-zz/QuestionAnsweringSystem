#!/usr/bin/env python3


from enum import Enum
from model import Question, QuestionType, AnswerType, LocationAttribute, TimeAttribute
import re


ATTRIBUTES_LIST = [
    "country",
    "product",
    "year",
    "named_entity",
    "action"
]


ATTRIBUTES = {
#place
    "country": ["russia", "japan", "germany"],
    "product": ["pycharm", "appcode", "rubymine", "resharper", "intellijidea"],
    "year": [],
    "named_entity": ["Microsoft", "JetBrains"],
    "action": ["released", "bought"]
}


SINONYMS = {
    "IntellIjidea": ["idea", "intellij idea", "intellijidea"],
    "PyCharm": ["pycharm"],
    "AppCode": ["appcode"],
    "RubyMine": ["rubymine"],
    "ReSharper": ["resharper"],
    "Russia": ["russia", "russian federation"],
    "Japan": ["japan", "land of the rising sun"],
    "Germany": ["germany", "federal republic of germany"],
}


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


def parse(question): #returns a list of question's attributes
    question = question.lower()
    result = {}
    result["country"] = get_attribute_country(question)
    result["named_entity"] = get_attribute_named_entity(question)
    result["action"] = get_attribute_action(question)
    result["year"] = get_attribute_year(question)
    result["product"] = get_attribute_product(question)
    return Question(question=question, question_type=get_question_type(question), answer_type=get_answer_type(question), attributes=result)


def get_attribute_action(question):
    return get_attribute_by_list(ATTRIBUTES["action"], question)


def get_attribute_named_entity(question):
    return get_attribute_by_list(ATTRIBUTES["named_entity"], question)


def get_attribute_country(question):
    return LocationAttribute(country=get_attribute_by_list(ATTRIBUTES["country"], question))


def get_attribute_product(question):
    return get_attribute_by_list(ATTRIBUTES["product"], question)


def get_attribute_by_list(attr_list, question):
    for word in attr_list:
        if word in question:
            return get_repr(word)


def get_repr(word):
    for repr in SINONYMS:
        if word in SINONYMS[repr]:
            return repr


def get_attribute_year(question):
    search_result = re.search('in (\d+)', question)
    if search_result is not None:
        time = search_result.group(1)
        return TimeAttribute(start=time, end=time)


def get_question_type(question):
    for word, q_type in TYPES["help_words"].items():
        if word in question:
            return q_type


def get_answer_type(question):
    for word, ans_type in TYPES["interrogative"].items():
        if word in question:
            return ans_type