#!/usr/bin/env python3

from src.attributes import parse
from src.dispatcher import Dispatcher


def process_question(question):
    return Dispatcher.find_answer(parse(question))


def run(question):
    print(process_question(question))
