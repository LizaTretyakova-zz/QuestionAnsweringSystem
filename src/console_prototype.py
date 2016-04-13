#!/usr/bin/env python3

import psycopg2
from attributes import parse
from model import Question
from dispatcher import Dispatcher


# TODO: make it a module and use the library
def process_question(question):
    return Dispatcher.find_answer(parse(question))


if __name__ == "__main__":
    questions = [
        "how many downloads were there in Russia?",
        "how many downloads were there in 2015?",
        "how many downloads were in 2016?",
        "how many downloads were in Russia in 2015?",
        "how many downloads were there in Nigeria in 2014?",
        "how many downloads were made in Russia and Germany?",
        "How many customers were in China in 2015?",
        "how many customers are there in Japan?",
        "How many customers are there in Japan?",
        "How many PyCharm downloads were made in 2014?",
        "How many times PyCharm was downloaded in 2015?",
        "When was DataGrip released?",
        "When is PyCon 2016?",
        "How many customers were since 2015?"
    ]

    for question in questions:
        print(question)
        print(process_question(question))
