#!/usr/bin/env python3

import psycopg2
from attributes import parse
from model import Question, TimeAttribute
from dispatcher import Dispatcher


# TODO: make it a module and use the library
def process_question(question):
    return Dispatcher.find_answer(parse(question))


if __name__ == "__main__":
    questions = [
        "How many downloads were made from Asia in 2015?",
        "How many customers bought PyCharm in European Union 2 years ago?",
        "How many times PyCharm was downloaded from North America?",
        "How many PyCharm downloads were made from Tirol?",
        "How many PyCharm downloads were made from Siberia?",
        "How many PyCharm downloads were made from Bavaria?",

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
        "How many downloads have been since 2015?",
        "how many downloads were 1 year ago?",
        "How many customers were since 2015?",

        "dkfsdlkgjhslkrghkrgjhlkj dkfjhgdlsfkjhg dfgjhkshg fgdsklhg?",
        "How many downloads of PyCharm were made from Russia in 2014?",
        "How many different products are downloaded from Russia?", # potentially okay question
        "How many downloads of PyCharm were made from Russia from 2013 to 2015?",
        "How many downloads of PyCharm were made from Russia between 2013 and 2015?",
        "What was the number of licences of PyCharm sold in Russia in 2014?",
        "What was the number of licences of PyCharm bought in Russia in 2014?",
        "What was the number of licences of PyCharm downloaded in Russia in 2014?",
        "What is the number of PyCharm downloads?",
        "Which number of clients bought PyCharm in 2014?",
        "Which number of clients downloaded PyCharm in 2014?",
        "What was the country of the latest PyCharm download?",
        "What was the time of the first PyCharm download?",
        "What number of countries is PyCharm downloaded from?",
        "When was the last PyCharm download?",
        "How many customers have been since 2000?",
        "How many downloads were from 2000 to 2016 except 2015?",
        "How many downloads were till 2016 without 2015?",
        "When have xamarin been downloaded?",
        "How many downloads of PyCharm were made from Munich in 2014?",
        "How many different products are downloaded from Saint Petersburg?", # potentially okay question
        "how many downloads were there in Munich and Saint Petersburg?",
        "How many customers were there in 2000 and 2011?"
    ]

    for question in questions:
        print(question)
        print(process_question(question))
        print("***")

#attribute = TimeAttribute()
#attribute.add_segment(500, 505)
#attribute.add_segment(10, 200)
#attribute.add_segment(8, 205)
#attribute.add_except_segment(9, 20)
#attribute.add_except_segment(40, 50)
#attribute.add_except_segment(199, 210)
#attribute.eval_real_segments()