from database_utils.base_wrapper import BaseWrapper
from src.model import AnswerType, QuestionType


class CustomersWrapper(BaseWrapper):
    def __init__(self):
        super().__init__()

    def ask(self, question):
        answer_type = question.answer_type
        question_type = question.question_type
        product = question.attributes.product
        date = question.attributes.time
        place = question.attributes.location
        #        print("money, ", answer_type, product, place, date, question_type)

        if answer_type is not AnswerType.NUMBER or question_type is not QuestionType.CUSTOMERS:
            return None

        cur = self.conn.cursor()

        ask_about_dates = ""
        if len(date.real_segments) != 0:
            ask_about_dates = "AND ("
            parts = []
            for i in range(len(date.real_segments)):
                parts.append("""(EXTRACT(YEAR FROM order_date) >= coalesce(%s, EXTRACT(YEAR FROM order_date)) OR (order_date is NULL AND %s is NULL))
                    AND (EXTRACT(YEAR FROM order_date) <= coalesce(%s, EXTRACT(YEAR FROM order_date)) OR (order_date is NULL AND %s is NULL))
                """)
            ask_about_dates += " OR ".join(parts)
            ask_about_dates += ")"

#        ask_phrase = """SELECT COUNT(DISTINCT customer_id) FROM
#        customers LEFT JOIN (orders LEFT JOIN purchases ON order_id = orders.id) ON customers.id = customer_id
#        WHERE ((upper(country) = upper(coalesce(%s, country))) OR (country is NULL AND %s is NULL))
#        """ + ask_about_dates + """
#        AND (upper(product) = upper(coalesce(%s, product)) OR (product is NULL AND %s is NULL));"""

        ask_phrase = """SELECT COUNT(DISTINCT customer_id) FROM
        customers LEFT JOIN (orders LEFT JOIN purchases ON order_id = orders.id) ON customers.id = customer_id
        WHERE ((upper(country) like upper(coalesce(%s, country))) OR (country is NULL AND %s is NULL))
        """ + ask_about_dates + """
        AND (upper(product) = upper(coalesce(%s, product)) OR (product is NULL AND %s is NULL));"""

        list_for_date = []
        for segment in date.real_segments:
            list_for_date.append(segment.start)
            list_for_date.append(segment.start)
            list_for_date.append(segment.end)
            list_for_date.append(segment.end)

        rows = []
        if place is None or place.countries is None or len(place.countries) is 0:
            country = None
            cur.execute(ask_phrase, [country, country] + list_for_date + [product, product])
            rows += list(cur.fetchall()[0])
        else:
            for country in place.countries:
                cur.execute(ask_phrase, [country, country] + list_for_date + [product, product])
                rows += list(cur.fetchall()[0])

        return sum(rows)
