#!/usr/bin/env python3

import psycopg2
from attributes import get_attribute_country
from attributes import get_attribute_product
from model import Question
from types_detect import QuestionType
from types_detect import get_answer_type
from types_detect import get_question_type


def process_question(question):
    question_type = get_question_type(question)
    answer_type = get_answer_type(question)
    country = get_attribute_country(question)
    product = get_attribute_product(question)
    return Question(question=question, question_type=question_type, answer_type=answer_type, attribute_country=country, attribute_product=product)

def get_answer(question):
    conn = psycopg2.connect(database="postgres", user="qa", password="ulizoturome", host="localhost")
    cur = conn.cursor()
    query = ""
    if question.question_type == QuestionType.DOWNLOADS:
        query = """select sum(amount) from downloads where country = '""" + question.attribute_country + """'"""
    cur.execute(query)
    return cur.fetchall()


if __name__ == "__main__":
    questions = [
        "how many downloads was there in Russia?"
    ]

    for question in questions:
        processed_question = process_question(question)
        print(processed_question)
        if processed_question.question_type is None or processed_question.answer_type == None:
            print("Sorry, the question is not clear enough. Would you mind repeating it, please?")
        else:
            print(get_answer(processed_question))