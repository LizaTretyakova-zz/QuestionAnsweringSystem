#!/usr/bin/env python3

from collections import namedtuple
from enum import Enum

Question = namedtuple("Question", [
    "question", "question_type", "answer_type",
    "attributes"
])

#attributes: country, product, year, named_entity, action


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

    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end


class LocationAttribute(BaseAttribute):
    type = "location"
    country = "true" # TODO: !!! DELETE THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TODO: It's here only because of compatibility with Nadya's code!!!!

    def __init__(self, loc_list = None, countries = None, city = None):
        super().__init__()
        self.location = loc_list
        self.countries = countries
        self.city = city


class ActionAttribute(BaseAttribute):
    type = "action"

    def __init__(self, action = None, other = None):
        super().__init__(self)
        self.main_action = action
        self.other = other


class Attributes:
    def __init__(self):
        self.country = None
        self.product = None
        self.year = None
        self.named_entity = None
        self.action = None

    def items(self):
        return (self.__dict__).items()

    def print(self):
        print(self.__dict__)
