from database_utils.base_wrapper import BaseWrapper
from src.model import AnswerType, QuestionType


class CustomersWrapper(BaseWrapper):
    def __init__(self):
        super().__init__()

    def ask(self, question):
        answer_type = question.answer_type
        question_type = question.question_type
        product = question.attributes.product
        data = question.attributes.time
        place = question.attributes.location
        #        print("money, ", answer_type, product, place, data, question_type)

        if answer_type is not AnswerType.NUMBER or question_type is not QuestionType.CUSTOMERS:
            return None

        cur = self.conn.cursor()

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
