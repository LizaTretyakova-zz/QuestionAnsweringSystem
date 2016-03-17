from sys import *
import re

import datetime
from enum import Enum
import psycopg2

class Answer_Type(Enum):
    person = 0
    description = 1
    count = 2
    explanation = 3
    place = 4
    time = 5


class Query:
    def __init__(self, words):
        self.answer_type = None
        self.words = words
        self.possible_dates = set()
        self.possible_countries = set()
        self.answer_type = None

    def set_answer_type(self, answer_type):
        self.answer_type = answer_type

    def find_time(self):
        for word in words:
            if word.isdigit():
                self.possible_dates.add(word)
        if len(self.possible_dates) == 0: self.possible_dates.add(None)

    def find_country(self):
        previous_word = None
        for word in words:
            if (previous_word == "in") and (ask_country_base(word) != 0):
                self.possible_countries.add(word)
            elif (word in download_words) and (ask_nation_base(previous_word) != 0):
                self.possible_countries.add(ask_nation_base(previous_word, "country"))
            previous_word = word
        if len(self.possible_countries) == 0: self.possible_countries.add(None)


class Query_event(Query):
    def __init__(self, words):
        Query.__init__(self, words)
        self.action = None
        self.participant = None

    def find_action(self):
        if self.words[1] == "is":
            if len(self.words) > 4 and self.words[3][-3:-1] == "ing":
                self.action = words[3]
        elif len(self.words) > 3:
            if not self.words[3].isdigit(): self.action = self.words[3]

    def find_participant(self):
        self.participant = self.words[2]

    def get_answer(self):
        self.find_country()
        self.find_time()
        self.find_participant()
        self.find_action()
        for country in self.possible_countries:
            for date in self.possible_dates:
                return ask_events_database(self.answer_type, country, date, self.participant, self.action)


class Query_money(Query):
    def __init__(self, words):
        Query.__init__(self, words)
        self.possible_products = set()

    def find_product(self):
        for word in words:
            if ask_product_base(word) != 0:
                self.possible_products.add(word)
        if len(self.possible_products) == 0: self.possible_products.add(None)

    def get_answer(self):
        self.find_country()
        self.find_time()
        self.find_product()
        for country in self.possible_countries:
            for date in self.possible_dates:
                for product in self.possible_products:
                    return ask_money_database(self.answer_type, country, date, product)


class Query_downloads(Query):
    def __init__(self, words):
        Query.__init__(self, words)
        self.possible_products = set()

    def find_product(self):
        for word in words:
            if ask_product_base(word) != 0:
                self.possible_products.add(word)
        if len(self.possible_products) == 0: self.possible_products.add(None)

    def get_answer(self):
        self.find_country()
        self.find_time()
        self.find_product()
        for country in self.possible_countries:
            for date in self.possible_dates:
                for product in self.possible_products:
                    return ask_download_database(self.answer_type, country, date, product)


countries = set(["China", "Japan"])
products = set(["PyCharm"])
download_words = {"downloads", "download", "downloaded"}

def ask_events_database(ask_word, country, date, participant, action):
    print("events, ", ask_word, participant, action, date)
    if ask_word is not Answer_Type.time:
        print("Wrong question type")
        return None
    try:
        conn = psycopg2.connect("dbname='postgres' user='anta' host='localhost' password='7578757'")
    except:
        print("I am unable to connect to the database")
        return None
    cur = conn.cursor()

    ask_fraze = """SELECT event_start_date, event_finish_date FROM events
WHERE ((place = coalesce(%s, place)) OR (place is NULL AND %s is NULL)) AND
(named_entity1 = coalesce(%s, named_entity1) OR named_entity2 = coalesce(%s, named_entity2) \
OR (named_entity1 is NULL AND %s is NULL) OR (named_entity2 is NULL AND %s is NULL)) \
AND (action = coalesce(%s, action) OR (action is NULL AND %s is NULL));"""
    print(ask_fraze)
    cur.execute(ask_fraze, [country, country, \
                            participant, participant, participant, participant, action, action])
    rows = list(cur.fetchall())
    return rows

def ask_download_database(ask_word, country, date, product):
    print("downloads, ", ask_word, product, country, date)
    if ask_word is not Answer_Type.count:
        print("Wrong question type")
        return None
    try:
        conn = psycopg2.connect("dbname='postgres' user='anta' host='localhost' password='7578757'")
    except:
        print("I am unable to connect to the database")
        return None
    cur = conn.cursor()

    if date is None:
        int_date = None
    else:
        int_date = int(date)

    ask_fraze = """SELECT count(*) FROM downloads
WHERE ((country = coalesce(%s, country)) OR (country is NULL AND %s is NULL)) AND
(EXTRACT(YEAR FROM download_date) = coalesce(%s, EXTRACT(YEAR FROM download_date)) OR (download_date is NULL AND %s is NULL)) \
AND (product = coalesce(%s, product) OR (product is NULL AND %s is NULL));"""
    print(ask_fraze)
    cur.execute(ask_fraze, [country, country, int_date, int_date, product, product])
    rows = list(cur.fetchall()[0])
    return rows


def ask_money_database(ask_word, country, date, product):
    print("money, ", ask_word, product, date, country)
    if ask_word is not Answer_Type.count:
        print("Wrong question type")
        return None
    try:
        conn = psycopg2.connect("dbname='postgres' user='anta' host='localhost' password='7578757'")
    except:
        print("I am unable to connect to the database")
        return None
    cur = conn.cursor()

    ask_fraze = """SELECT count(*) FROM
(purchases INNER JOIN orders ON order_id = orders.id) INNER JOIN customers ON customers.id = customer_id
WHERE ((country = coalesce(%s, country)) OR (country is NULL AND %s is NULL)) AND
(EXTRACT(YEAR FROM order_date) = coalesce(%s, EXTRACT(YEAR FROM order_date)) OR (order_date is NULL AND %s is NULL)) \
AND (product = coalesce(%s, product) OR (product is NULL AND %s is NULL));"""
    print(ask_fraze)
    if date is None:
        int_date = None
    else:
        int_date = int(date)
    cur.execute(ask_fraze, [country, country, int_date, int_date, product, product])
    rows = list(cur.fetchall()[0])
    return rows


def ask_nation_base(word, retrun_group=None):
    if retrun_group is not None:
        return "a"
    else:
        return False


def ask_country_base(word, retrun_group=None):
    if retrun_group is not None:
        return "a"
    else:
        if word in countries:
            return True
        else:
            return False


def ask_product_base(word, retrun_group=None):
    if word in products:
        return True
    else:
        return False


def who_function(words):
    return Answer_Type.person


def what_function(words):
    return Answer_Type.description


def how_function(words):
    if words[1] == "many" or words[1] == "much":
        return Answer_Type.count
    return Answer_Type.explanation


def where_function(words):
    return Answer_Type.place


def when_function(words):
    return Answer_Type.time


ask_word_function_mapping = {
    "Who": who_function,
    "What": what_function,
    "How": how_function,
    "Where": where_function,
    "When": when_function,
}


def detect_question_subject(words):
    for word in words:
        if word in download_words:
            return Query_downloads(words)
    if words[0] == "How" and (words[1] == "much" or words[1] == "many"):
        return Query_money(words)
    return Query_event(words)


def detect_answer_type(words):
    return ask_word_function_mapping[words[0]](words)


if __name__ == "__main__":
    words = raw_input().split()
    words[-1] = re.match('(\w)*', words[-1]).group(0)
    print(words)
    question_subject = detect_question_subject(words)
    answer_type = detect_answer_type(words)
    question_subject.set_answer_type(answer_type)
    print(question_subject.get_answer())
    print