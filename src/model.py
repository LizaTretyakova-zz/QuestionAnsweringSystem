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


class Segment(object):

    max_year = int(1e10)

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def __cmp__(self, other):
        return self.start < other.start

    def __repr__(self):
        return self.__dict__.__repr__()

    def intersect(self, s2):
        if self.start > s2.end or self.end < s2.start:
            return False
        return True

    def not_none(self):
        if self.start is None:
            self.start = 0
        if self.end is None:
            self.end = self.max_year
        return self


class TimeAttribute(BaseAttribute):
    type = "time"

    def __init__(self, start=None, end=None, proposition=None, except_date=None,
                 except_prepositions=None):
        super().__init__()
        self.start = start
        self.end = end
        self.proposition = proposition
        self.except_date = except_date
        self.segment_list = []
        self.except_prepositions = except_prepositions
        self.except_segment_list = []
        self.real_segments = []

    def add_segment(self, start=None, end=None):
        self.segment_list.append(Segment(start=start, end=end).not_none())

    def add_except_segment(self, start=None, end=None):
        self.except_segment_list.append(Segment(start=start, end=end).not_none())

    def eval_real_segments(self):
        self.real_segments = self.segment_list
        for except_segment in self.except_segment_list:
            additional_segments = list(self.real_segments)
            for segment in additional_segments:
                if except_segment.intersect(segment):
                    self.real_segments.remove(segment)
                    if except_segment.start > segment.start:
                        segment_for_add = Segment(segment.start, except_segment.start - 1)
                        self.real_segments.append(segment_for_add)
                    if except_segment.end < segment.end:
                        segment_for_add = Segment(except_segment.end + 1, segment.end)
                        self.real_segments.append(segment_for_add)
        self.real_segments.sort(key=lambda x: x.start)
        for i in range(1, len(self.real_segments)):
            if self.real_segments[i - 1].intersect(self.real_segments[i]):
                new_segment = Segment(self.real_segments[i - 1].start, self.real_segments[i].end)
                self.real_segments[i - 1] = new_segment
                self.real_segments[i] = new_segment
        self.real_segments = list(set(self.real_segments))

    def __repr__(self):
        return self.__dict__.__repr__()


class LocationAttribute(BaseAttribute):
    type = "location"

    def __init__(self, locations=None, countries=None, cities=None):
        super().__init__()
        self.locations = locations
        self.countries = countries
        self.cities = cities

    def __repr__(self):
        return self.__dict__.__repr__()


class ActionAttribute(BaseAttribute):
    type = "action"

    def __init__(self, action_lemma=None, action=None, other=None, auxiliary=None):
        super().__init__()
        self.action_lemma = action_lemma
        self.action = action
        self.other = other
        self.auxiliary = auxiliary

    def __repr__(self):
        return self.__dict__.__repr__()


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

    def printf(self):
        print(self.__dict__)
        print("Location: ", end='')
        print("location = ", end='')
        print(self.location.locations, end='')
        print(" countries = ", end='')
        print(self.location.countries, end='')
        print(" cities = ", end='')
        print(self.location.cities)
