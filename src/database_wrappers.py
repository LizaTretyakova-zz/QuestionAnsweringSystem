from model import QuestionType, AnswerType, BaseAttribute
import psycopg2


class BaseWrapper:
    def __init__(self):
        pass


class DownloadsWrapper:
    DEFAULT_COUNTRY_VALUE = True
    DEFAULT_TIME_VALUE = [True]
    DEFAULT_QUERY_VALUE = "%s"

    def __init__(self, question):
        self.question = question  # COUNTRY, product, DOWNLOAD_DATE, amount
        self.country = self.DEFAULT_COUNTRY_VALUE
        self.time = self.DEFAULT_TIME_VALUE
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
            elif attr.type == "location" and attr.country is not None:
                self.country = attr.country
                self.query_country = "country = %s"
            elif attr.type == "time":
                if attr.start is not None and attr.end is not None and attr.start == attr.end:
                    self.time = [attr.start]
                    self.query_duration = " extract(year from download_date) = %s"
                elif attr.start is not None and attr.end is not None:
                    self.time = [attr.start, attr.end]
                    self.query_duration = "extract(year from download_date) between %s and %s"
                elif attr.start is not None:
                    self.time = [attr.start]
                    self.query_duration = "extract(year from download_date) > %s"
                elif attr.end is not None:
                    self.time = [attr.end]
                    self.query_duration = "extract(year from download_date) < %s"
        # if self.query_country is None:
        #     self.country = True
        #     self.query_country = "%s"
        # if self.query_duration is None:
        #     self.time = [True]
        #     self.query_duration = "%s"

    def __create_query__(self):
        self.query = "select sum(amount) from downloads where " + self.query_country + " and " + self.query_duration

    def __create_arguments__(self):
        if len(self.time) > 1:
            self.arguments = (self.country, self.time[0], self.time[1])
        else:
            self.arguments = (self.country, self.time[0])

    def get(self):
        self.__extract_data__()
        self.__create_query__()
        self.__create_arguments__()
        conn = psycopg2.connect(database="postgres", user="qa", password="ulizoturome", host="localhost")

        # if self.question.subtype == QuestionSubtype.AMOUNT:
        cur = conn.cursor()
        cur.execute(self.query, self.arguments)
        res = cur.fetchone()
        message = "Success"
        if res[0] is None:
            message = """Sorry, we currently do not have any information"""
            if self.country is not self.DEFAULT_COUNTRY_VALUE or self.time is not self.DEFAULT_TIME_VALUE:
                message += """ about """
                if self.country is not self.DEFAULT_COUNTRY_VALUE and self.time is not self.DEFAULT_TIME_VALUE:
                    message += self.country + """ in specified time"""
                elif self.country is not self.DEFAULT_COUNTRY_VALUE:
                    message += self.country
                else:
                    message += """specified time"""
            message += """. Try to change the country or time restrictions."""
        return {"result": res, "message": message}
