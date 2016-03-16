#!/usr/bin/env python3
from model import Question
#TODO: PARSER -- gets all the attributes it can


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


def parse(question): #returns a list of question's attributes
    question = question.lower()
    result = {}
    result["country"] = get_attribute_country(question)
    result["named_entity"] = get_attribute_named_entity(question)
    result["action"] = get_attribute_action(question)
#    result["year"] = to be done
    result["product"] = get_attribute_product(question)
    return Question(question=question, question_type=None, answer_type=None, attributes=result)

#def get_attribute_year(question):
#TODO to be implemented


def get_attribute_action(question):
    return get_attribute_by_list(ATTRIBUTES["action"], question)


def get_attribute_named_entity(question):
    return get_attribute_by_list(ATTRIBUTES["named_entity"], question)


def get_attribute_country(question):
    return get_attribute_by_list(ATTRIBUTES["country"], question)


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

