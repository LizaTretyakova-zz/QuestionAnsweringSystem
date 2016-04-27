import psycopg2

from base_wrapper import BaseWrapper, USER, PASSWORD
from model import BaseAttribute


class DownloadsWrapper(BaseWrapper):
    DEFAULT_VALUE = [True]
    DEFAULT_QUERY_VALUE = "%s"

    def __init__(self, question):
        super().__init__()
        self.question = question  # COUNTRY, product, DOWNLOAD_DATE, amount
        self.country = self.DEFAULT_VALUE
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
            elif attr.type == "location" and attr.countries is not None:
                if attr.countries:
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
                if self.country is not self.DEFAULT_VALUE and self.time is not self.DEFAULT_VALUE:
                    message += ", ".join(self.country) + """ in specified time"""
                elif self.country is not self.DEFAULT_VALUE:
                    message += ", ".join(self.country)
                else:
                    message += """specified time"""
            message += """. Try to change the country or time restrictions."""
        return {"result": res, "message": message}
