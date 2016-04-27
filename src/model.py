#!/usr/bin/env python3

from collections import namedtuple
from enum import Enum

Question = namedtuple("Question", [
    "question", "question_type", "answer_type",
    "attributes"
])


# attributes: country, product, year, named_entity, action


class AnswerType(Enum):
    NUMBER = 0
    DATE = 1


class QuestionType(Enum):
    DOWNLOADS = 0
    CUSTOMERS = 1
    EVENTS = 2
    SALES = 3


class BaseAttribute:
    type = "Base"
    is_iterate = False

    def __next__(self):
        if not self.is_iterate:
            self.is_iterate = True
            return self
        raise StopIteration

    def __iter__(self):
        return self

    def __init__(self):
        pass


class TimeAttribute(BaseAttribute):
    type = "time"

    def __init__(self, start=None, end=None, proposition=None, except_date=None,
                 except_prepositions=None):
        super().__init__()
        self.start = start
        self.end = end
        self.proposition = proposition
        self.except_date = except_date
        self.except_prepositions = except_prepositions

    def __repr__(self):
        return (self.__dict__).__repr__()


class LocationAttribute(BaseAttribute):
    type = "location"

    def __init__(self, loc_list=None, countries=None, city=None):
        super().__init__()
        self.location = loc_list
        self.countries = countries
        self.city = city

    def __repr__(self):
        return (self.__dict__).__repr__()


class ActionAttribute(BaseAttribute):
    type = "action"

    def __init__(self, action=None, other=None, auxiliary= None):
        super().__init__()
        self.main_action = action
        self.other = other
        self.auxiliary = auxiliary


class Attributes:
    def __init__(self):
        self.location = None
        self.product = None
        self.time = None
        self.named_entity = None
        self.action = None

    def items(self):
        return (self.__dict__).items()

    def __repr__(self):
        return (self.__dict__).__repr__()
