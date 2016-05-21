from database_utils.base_wrapper import BaseWrapper
from src.model import BaseAttribute, Question

import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)


class DownloadsWrapper(BaseWrapper):
    DEFAULT_VALUE = [True]
    NEGATIVE_VALUE = [False]
    DEFAULT_QUERY_VALUE = "%s"

    def __init__(self):
        super().__init__()
        self._drop_fields_values_()

    def _drop_fields_values_(self):
        self.question = None
        self.country = self.DEFAULT_VALUE
        self.location = self.DEFAULT_VALUE
        self.city = self.DEFAULT_VALUE
        self.time = self.DEFAULT_VALUE
        self.arguments = None
        self.query = None
        self.query_country = self.DEFAULT_QUERY_VALUE  # list of countries is temporary not supported
        self.query_duration = self.DEFAULT_QUERY_VALUE  # list of separate years is temporary not supported, but [), (], [] are

    def _extract_data_(self):
        if self.question is None:
            return "No question provided."
        for attr_name, attr in self.question.attributes.items():
            if not isinstance(attr, BaseAttribute):
                pass
            elif attr.type == "location":  # and attr.countries is not None:
                # if attr.locations:
                #     self.location = attr.locations
                # if attr.cities:
                #     self.city = attr.cities
                if not attr.countries:
                    self.country = self.NEGATIVE_VALUE
                else:
                    self.country = [x.upper() for x in attr.countries]
                    # self.country = attr.countries
                    self.query_country = "upper(country) in %s"
                    # self.query_country = "(country = %s " + "or country = %s " * (len(attr.countries) - 1) + ") "
            elif attr.type == "time":
                if self.time is self.DEFAULT_VALUE and len(attr.real_segments) > 0:
                    self.time = []
                for segment in attr.real_segments:
                    self.query_duration = \
                        ("(" if self.query_duration == self.DEFAULT_QUERY_VALUE else (self.query_duration + " or "))
                    if segment.start is not None and segment.end is not None and segment.start == segment.end:
                        self.time.extend([segment.start])
                        self.query_duration += " extract(year from download_date) = %s"
                    elif segment.start is not None and segment.end is not None:
                        self.time.extend([segment.start, segment.end])
                        self.query_duration += " extract(year from download_date) between %s and %s"
                    elif segment.start is not None:
                        self.time.extend([segment.start])
                        self.query_duration += " extract(year from download_date) > %s"
                    elif attr.end is not None:
                        self.time.extend([segment.end])
                        self.query_duration += " extract(year from download_date) < %s"
                if len(attr.real_segments) > 0:
                    self.query_duration += ")"

    def __create_query__(self):
        self.query = "select sum(amount) from downloads where " + self.query_country + " and " + self.query_duration

    def __create_arguments__(self):
        self.arguments = tuple([tuple(self.country)] + self.time)

    def get(self, question: Question):
        self._drop_fields_values_()
        self.question = question

        self._extract_data_()
        self.__create_query__()
        #
        logging.debug(question.attributes.time)
        #
        self.__create_arguments__()

        cur = self.conn.cursor()
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
