#!/usr/bin/env python3
import psycopg2
import spacy.en
import attribute_utils
from src.model import Question, Attributes


def parse(question: str) -> Question:  # returns a list of question's attributes
    # question is a string
    # doc is spacy-parsed question

    try:
        parse.nlp
    except AttributeError:
        parse.nlp = spacy.en.English()

    doc = parse.nlp(question)
    result = Attributes()
    try:
        result.location = attribute_utils.get_attribute_location_spacy(doc)
        result.named_entity = attribute_utils.get_attribute_named_entity(question)
        result.time = attribute_utils.get_attribute_time_spacy(doc, question)
        result.action = attribute_utils.get_attribute_action(doc)
        result.product = attribute_utils.get_attribute_product(question)
    except KeyError as e:
        print("KeyError. Json config doesn't contain such key:", str(e))
        return None
    except psycopg2.OperationalError as e:
        print("Error during database operation:\n", str(e))
        return None
    return Question(
        question=question,
        question_type=attribute_utils.get_question_type(question, result.action),
        answer_type=attribute_utils.get_answer_type(question),
        attributes=result
    )
