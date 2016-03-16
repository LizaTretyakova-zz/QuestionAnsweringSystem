#!/usr/bin/env python3

from collections import namedtuple

Question = namedtuple("Question", [
    "question", "question_type", "answer_type",
    "attributes"
])

#attributes: country, product, year, named_entity, action
