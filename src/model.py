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
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def __cmp__(self, other):
        return self.start < other.start

    def __repr__(self):
        return self.__dict__.__repr__()


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
        self.segment_list.append(Segment(start=start, end=end))

    def add_except_segment(self, start=None, end=None):
        self.except_segment_list.append(Segment(start=start, end=end))

    def eval_real_segments(self):
        self.segment_list.sort(key=lambda x: x.start)
        self.except_segment_list.sort(key=lambda x: x.start)
        cur_except_segment = 0
        except_segment = self.except_segment_list[cur_except_segment]

        for segment in self.segment_list:
            while cur_except_segment < len(self.except_segment_list) and \
                            except_segment.end < segment.start:
                except_segment = self.except_segment_list[cur_except_segment]
                cur_except_segment += 1
            while cur_except_segment < len(self.except_segment_list) and \
                            except_segment.start < segment.end:
                if segment.end < except_segment.start or segment.start > except_segment.end:
                    self.real_segments.append(Segment(segment.start, segment.end))
                    continue
                if except_segment.start <= segment.start and except_segment.end >= segment.end:
                    continue
                if segment.start < except_segment.start:
                    self.real_segments.append(Segment(segment.start, except_segment.start))
                if segment.end > except_segment.end:
                    self.real_segments.append(Segment(except_segment.end, segment.end))
                except_segment = self.except_segment_list[cur_except_segment]
                cur_except_segment += 1
        print(self.real_segments)

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
