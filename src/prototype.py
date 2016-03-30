import psycopg2
import re

#import nltk
from enum import Enum

#from nltk.corpus import *


class Answer_Type(Enum):
    person = 0
    description = 1
    count = 2
    explanation = 3
    place = 4
    time = 5

countries = {"China", "Japan"}
products = {"PyCharm"}
download_words = {"downloads", "download", "downloaded"}


class MetaData():
    country = None
    year = None
    named_entity1 = None
    named_entity2 = None
    product = None
    action = None
    answer_type = None

    def __init__(self):
        self.country = set()
        self.year = set()
        self.named_entity1 = set()
        self.named_entity2 = set()
        self.product = set()
        self.action = set()

#    def __init__(self, country, year, named_entity1, named_entity2, product, action, answer_type):
#        self.country = country
#        self.year = year
#        self.named_entity1 = named_entity1
#        self.named_entity2 = named_entity2
#        self.product = product
#        self.action = action
#        self.answer_type = answer_type


class WrapperEventDatabase(object):
    @staticmethod
    def ask(meta_data):
        answer_type = meta_data.answer_type
        participant = meta_data.named_entity1
        action = meta_data.action
        year = meta_data.year
        country = meta_data.country
        print("events, ", answer_type, participant, action, year)
        if answer_type is None or answer_type is not Answer_Type.time:
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
        cur.execute(ask_fraze, [country, country, \
                                participant, participant, participant, participant, action, action])
        rows = list(cur.fetchall())
        return rows


class WrapperDownloadDatabase(object):
    @staticmethod
    def ask(meta_data):
        answer_type = meta_data.answer_type
        product = meta_data.named_entity1
        country = meta_data.country
        year = meta_data.year
        print("downloads, ", answer_type, product, country, year)
        if answer_type is not Answer_Type.count:
            return None
        try:
            conn = psycopg2.connect("dbname='postgres' user='anta' host='localhost' password='7578757'")
        except:
            print("I am unable to connect to the database")
            return None
        cur = conn.cursor()

        if year is None:
            int_date = None
        else:
            int_date = int(year)

        ask_fraze = """SELECT count(*) FROM downloads
    WHERE ((country = coalesce(%s, country)) OR (country is NULL AND %s is NULL)) AND
    (EXTRACT(YEAR FROM download_date) = coalesce(%s, EXTRACT(YEAR FROM download_date)) OR (download_date is NULL AND %s is NULL)) \
    AND (product = coalesce(%s, product) OR (product is NULL AND %s is NULL));"""
        cur.execute(ask_fraze, [country, country, int_date, int_date, product, product])
        rows = list(cur.fetchall()[0])
        return rows


class WrapperMoneyDatabase(object):
    @staticmethod
    def ask(meta_data):
        answer_type = meta_data.answer_type
        product = meta_data.product
        year = meta_data.year
        country = meta_data.country
        print((answer_type, product, year, country))
        print("money, ", answer_type, product, year, country)
        if answer_type is not Answer_Type.count:
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
        if year is None:
            int_date = None
        else:
            int_date = int(year)
        cur.execute(ask_fraze, [country, country, int_date, int_date, product, product])
        rows = list(cur.fetchall()[0])
        return rows


databases_ask_functions = (
    WrapperDownloadDatabase.ask,
    WrapperEventDatabase.ask,
    WrapperMoneyDatabase.ask
)


def ask_nation_base(word, return_group=None):
    if return_group is not None:
        return "a"
    else:
        return False


def ask_country_base(word, return_group=None):
    if return_group is not None:
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


class Analysis(object):
    meta_data = MetaData()
    words = None

    def __init__(self, sentence):
        self.words = sentence

    class QuestionClassification(object):
        @staticmethod
        def who_function(sentence):
            return Answer_Type.person

        @staticmethod
        def what_function(sentence):
            return Answer_Type.description

        @staticmethod
        def how_function(sentence):
            if sentence[1] == "many" or sentence[1] == "much":
                return Answer_Type.count
            return Answer_Type.explanation

        @staticmethod
        def where_function(sentence):
            return Answer_Type.place

        @staticmethod
        def when_function(sentence):
            return Answer_Type.time

        @staticmethod
        def get_answer_type(words):
            ask_word_function_mapping = {
                "Who": Analysis.QuestionClassification.who_function,
                "What": Analysis.QuestionClassification.what_function,
                "How": Analysis.QuestionClassification.how_function,
                "Where": Analysis.QuestionClassification.where_function,
                "When": Analysis.QuestionClassification.when_function,
            }
            return ask_word_function_mapping[words[0]](words)

    class QueryAnalyzer(object):
        @staticmethod
        def find_country(sentence):
            previous_word = None
            for word in sentence:
                if (previous_word == "in") and (ask_country_base(word) != 0):
                    Analysis.meta_data.country.add(word)
                elif (word in download_words) and (ask_nation_base(previous_word) != 0):
                    Analysis.meta_data.country.add(ask_nation_base(previous_word, "country"))
                previous_word = word
            if len(Analysis.meta_data.country) == 0: Analysis.meta_data.country.add(None)

        @staticmethod
        def find_product(sentence):
            for word in sentence:
                if ask_product_base(word) != 0:
                    Analysis.meta_data.product.add(word)
            if len(Analysis.meta_data.product) == 0: Analysis.meta_data.product.add(None)

        @staticmethod
        def find_action(words):
#            wsj = nltk.corpus.treebank.tagged_words(tagset='universal')
#            word_tag_fd = nltk.FreqDist(wsj)
#            return set([wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'VERB'])
            if words[1] == "is" or words[1] == "are":
                if len(words) > 4 and words[3][-3:-1] == "ing":
                    Analysis.meta_data.action.add(words[3])
                else:
                    Analysis.meta_data.action.add(words[1])
            elif len(words) > 3:
                if not words[3].isdigit():
                    Analysis.meta_data.action.add(words[3])

        @staticmethod
        def find_time(sentence):
            for word in sentence:
                if word.isdigit():
                    Analysis.meta_data.year.add(word)
            if len(Analysis.meta_data.year) is 0: Analysis.meta_data.year.add(None)

        @staticmethod
        def find_named_entity1(sentence):
            Analysis.meta_data.named_entity1.add(sentence[2])

        @staticmethod
        def find_named_entity2(sentence):
            Analysis.meta_data.named_entity2.add(None)

    def analyze(self):
        Analysis.QueryAnalyzer.find_country(self.words)
        Analysis.QueryAnalyzer.find_product(self.words)
        Analysis.QueryAnalyzer.find_action(self.words)
        Analysis.QueryAnalyzer.find_named_entity1(self.words)
        Analysis.QueryAnalyzer.find_named_entity2(self.words)
        Analysis.QueryAnalyzer.find_time(self.words)
        Analysis.meta_data.answer_type = Analysis.QuestionClassification.get_answer_type(self.words)


class Dispatcher(object):
    @staticmethod
    def find_answer(meta_data):
        possible_answers = []
        cur_data = MetaData()
        cur_data.answer_type = Analysis.meta_data.answer_type
        is_question_right_format = False
        for country in meta_data.country:
            cur_data.country = country
            for year in meta_data.year:
                cur_data.year = year
                for named_entity1 in meta_data.named_entity1:
                    cur_data.named_entity1 = named_entity1
                    for named_entity2 in meta_data.named_entity2:
                        cur_data.named_entity2 = named_entity2
                        for product in meta_data.product:
                            cur_data.product = product
                            for action in meta_data.action:
                                cur_data.action = action
                                for func in databases_ask_functions:
                                    answer = func(cur_data)
                                    if answer is not None:
                                        is_question_right_format = True
                                        possible_answers.append(answer)
        if is_question_right_format:
            return possible_answers
        else:
            print("Wrong question type")
            return None


def query(words):
    analyzer = Analysis(words)
    analyzer.analyze()
    print("action " + str(Analysis.meta_data.action))
    print("year " + str(Analysis.meta_data.year))
    print("product " + str(Analysis.meta_data.product))
    print("answer_type " + str(Analysis.meta_data.answer_type))
    print("country " + str(Analysis.meta_data.country))
    return Dispatcher.find_answer(Analysis.meta_data)

if __name__ == "__main__":
    words = input().split()
    words[-1] = re.match('(\w)*', words[-1]).group(0)
    print(words)
    print(query(words))
    print('\n')