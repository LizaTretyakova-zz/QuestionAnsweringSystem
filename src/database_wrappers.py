from attributes import QuestionType
import psycopg2

def get_from_downloads(question):
    conn = psycopg2.connect(database="postgres", user="qa", password="ulizoturome", host="localhost")
    cur = conn.cursor()
    query = """select sum(amount) \
               from downloads \
               where lower(country) = coalesce(lower(%s), lower(country)) \
               and extract(year from download_date) = coalesce(%s, extract(year from download_date))"""
    cur.execute(query, (question.attributes["country"], question.attributes["year"]))
    return cur.fetchall()
