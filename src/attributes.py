#!/usr/bin/env python3


ATTRIBUTES = {
    "country": ["russia", "japan", "germany"],
    "product": ["pycharm", "appcode", "rubymine", "resharper", "intellijidea"]
}

SINONYMS = {
    "intellijidea": ["idea", "intellij idea", "intellijidea"],
    "pycharm": ["pycharm"],
    "appcode": ["appcode"],
    "rubymine": ["rubymine"],
    "resharper": ["resharper"],
    "russia": ["russia", "russian federation"],
    "japan": ["japan", "land of the rising sun"],
    "germany": ["germany", "federal republic of germany"]
}

def get_attribute_country(question):
    return get_attribute(ATTRIBUTES["country"], question)

def get_attribute_product(question):
    return get_attribute(ATTRIBUTES["product"], question)

def get_attribute(attr_list, question):
    for word in attr_list:
        if word in question:
            return get_repr(word)
    return ""

def get_repr(word):
    for repr in SINONYMS:
        if word in SINONYMS[repr]:
            return repr

