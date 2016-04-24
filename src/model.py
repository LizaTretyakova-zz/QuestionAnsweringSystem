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

    def __init__(self, start=None, end=None, proposition=None):
        super().__init__()
        self.start = start
        self.end = end
        self.proposition = proposition


class LocationAttribute(BaseAttribute):
    type = "location"

    def __init__(self, locations=None, countries=None, cities=None):
        super().__init__()
        self.locations = locations
        self.countries = countries
        self.cities = cities


class ActionAttribute(BaseAttribute):
    type = "action"

    def __init__(self, action_lemma=None, action=None, other=None, auxiliary= None):
        super().__init__()
        self.action_lemma = action_lemma
        self.action = action
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

    def print(self):
        print(self.__dict__)
        print("Location: ", end='')
        print("location = ", end='')
        print(self.location.locations, end='')
        print(" countries = ", end='')
        print(self.location.countries, end='')
        print(" cities = ", end='')
        print(self.location.cities)

