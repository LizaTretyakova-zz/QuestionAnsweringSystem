#!/usr/bin/env python3

import psycopg2
from attributes import parse
from model import Question
from dispatcher import dispatch

#TODO: make it a module and use the library
def process_question(question):
    return dispatch(parse(question))

if __name__ == "__main__":
    questions = [
        "how many downloads were there in Russia?",
        "how many downloads were there in 2015?",
        "how many downloads were in 2016?",
        "how many downloads were there in Nigeria in 2014?"
    ]

    for question in questions:
        print(process_question(question))


#TODO:
# нормальная генерация запросов,
# парсер вопроса, который возвращает типы, атрибуты, источник данных(!)
# и другая сущность, которая по этой распаршенной штуке выдаёт готовый ответ --
#  внутри себя тихо обращаясь к базе данных
            # база                      база                        база
            # класс-обёртка над ней     класс-обёртка над ней       класс-обёртка над ней (могут наследоваться от чего-то общего)
            # ^почему бы ему не знать всё о полях своей таблицы?)
            #
            #                                       диспетчер [@@@] -- пытается найти информацию по нашему вопросу. Например, спрашивать все таблички, знают ли они чего про Васю
            #                                                        ^
            #                                                        |
            # предложение ----идет на вход----> [лексер-парсер] -> (type: count/date/etc, entities: <слово из вопроса, Васи какие-нибудь>, ...)
            # здесь надо использовать библиотеку, и из разбора предложения понимать entities.