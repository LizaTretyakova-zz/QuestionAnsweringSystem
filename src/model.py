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
    MONEY = 1
    EVENTS = 2



class BaseAttribute:
    type = "Base"

    def __init__(self):
        pass


class TimeAttribute(BaseAttribute):
    type = "time"
    start = None
    end = None

    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end


class LocationAttribute(BaseAttribute):
    type = "location"
    country = None
    city = None

    def __init__(self, country = None, city = None):
        super().__init__()
        self.country = country
        self.city = city