from model import QuestionType, AnswerType, BaseAttribute
import psycopg2


USER = "demo"
PASSWORD = "demo"

class BaseWrapper:
    def __init__(self):
        pass


class DownloadsWrapper:
    DEFAULT_VALUE = [True]
    NEGATIVE_VALUE = [False]
    DEFAULT_QUERY_VALUE = "%s"

    def __init__(self, question):
        self.question = question  # COUNTRY, product, DOWNLOAD_DATE, amount
        self.country = self.DEFAULT_VALUE
        # self.location = self.DEFAULT_VALUE
        # self.city = self.DEFAULT_VALUE
        self.time = self.DEFAULT_VALUE
        self.arguments = None
        self.query = None
        self.query_country = self.DEFAULT_QUERY_VALUE  # list of countries is temporary not supported
        self.query_duration = self.DEFAULT_QUERY_VALUE  # list of separate years is temporary not supported, but [), (], [] are

    def __extract_data__(self):
        if self.question is None:
            return "No question provided."
        for attr_name, attr in self.question.attributes.items():
            if not isinstance(attr, BaseAttribute):
                pass
            elif attr.type == "location": # and attr.countries is not None:
                # if attr.locations:
                #     self.location = attr.locations
                # if attr.cities:
                #     self.city = attr.cities
                if not attr.countries:
                    self.country = self.NEGATIVE_VALUE
                else:
                    self.country = attr.countries
                    self.query_country = "country in %s"
                    # self.query_country = "(country = %s " + "or country = %s " * (len(attr.countries) - 1) + ") "
            elif attr.type == "time":
                if attr.start is not None and attr.end is not None and attr.start == attr.end:
                    self.time = [attr.start]
                    self.query_duration = " extract(year from download_date) = %s"
                elif attr.start is not None and attr.end is not None:
                    self.time = [attr.start, attr.end]
                    self.query_duration = " extract(year from download_date) between %s and %s"
                elif attr.start is not None:
                    self.time = [attr.start]
                    self.query_duration = " extract(year from download_date) > %s"
                elif attr.end is not None:
                    self.time = [attr.end]
                    self.query_duration = " extract(year from download_date) < %s"

    def __create_query__(self):
        self.query = "select sum(amount) from downloads where " + self.query_country + " and " + self.query_duration

    def __create_arguments__(self):
        self.arguments = tuple([tuple(self.country)] + self.time)

    def get(self):
        self.__extract_data__()
        self.__create_query__()
        self.__create_arguments__()
        conn = psycopg2.connect(database="postgres", user=USER, password=PASSWORD, host="localhost")

        cur = conn.cursor()
        cur.execute(self.query, self.arguments)
        res = cur.fetchone()
        message = "Success"
        if res[0] is None:
            message = """Sorry, we currently do not have any information"""
            if self.country is not self.DEFAULT_VALUE or self.time is not self.DEFAULT_VALUE:
                message += """ about """
                if self.country is not self.DEFAULT_VALUE \
                        and self.country is not self.NEGATIVE_VALUE \
                        and self.time is not self.DEFAULT_VALUE:
                    message += ", ".join(self.country) + """ in specified time"""
                elif self.country is not self.DEFAULT_VALUE and self.country is not self.NEGATIVE_VALUE:
                    message += ", ".join(self.country)
                elif self.country is not self.DEFAULT_VALUE:
                    message += """specified location"""
                else:
                    message += """specified time"""
            message += """. Try to change the country or time restrictions."""
        return {"result": res, "message": message}


class WrapperMoneyDatabase(object):
    @staticmethod
    def ask(question):
        answer_type = question.answer_type
        question_type = question.question_type
        product = question.attributes.product
        data = question.attributes.time
        place = question.attributes.location
        #        print("money, ", answer_type, product, place, data, question_type)

        if answer_type is not AnswerType.NUMBER or question_type is not QuestionType.CUSTOMERS:
            return None
        try:
            conn = psycopg2.connect(database='postgres', user=USER, host='localhost', password=PASSWORD)
        except:
            print("I am unable to connect to the database")
            return None
        cur = conn.cursor()

        ask_phrase = """SELECT count(*) FROM
    (purchases INNER JOIN orders ON order_id = orders.id) INNER JOIN customers ON customers.id = customer_id
    WHERE ((country = coalesce(%s, country)) OR (country is NULL AND %s is NULL)) AND
    (EXTRACT(YEAR FROM order_date) >= coalesce(%s, EXTRACT(YEAR FROM order_date)) OR (order_date is NULL AND %s is NULL)) \
    AND \
    (EXTRACT(YEAR FROM order_date) <= coalesce(%s, EXTRACT(YEAR FROM order_date)) OR (order_date is NULL AND %s is NULL)) \
    AND (product = coalesce(%s, product) OR (product is NULL AND %s is NULL));"""

        if data is None:
            year_end = None
            year_start = None
        else:
            if data.start is None:
                year_start = None
            else:
                year_start = int(data.start)
            if data.end is None:
                year_end = None
            else:
                year_end = int(data.end)
        rows = []
        if place is None or place.countries is None or len(place.countries) is 0:
            country = None
            cur.execute(ask_phrase, [country, country, year_start, year_start, \
                                     year_end, year_end, product, product])
            rows += list(cur.fetchall()[0])
        else:
            for country in place.countries:
                cur.execute(ask_phrase, [country, country, year_start, year_start, \
                                         year_end, year_end, product, product])
                rows += list(cur.fetchall()[0])
        return sum(rows)
