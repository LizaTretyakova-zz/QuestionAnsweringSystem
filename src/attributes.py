#!/usr/bin/env python3
import psycopg2
import spacy.en
import attribute_utils
from src.model import Question, Attributes

import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import config
logger = config.get_logger()


def parse(question: str) -> Question:  # returns a list of question's attributes
    try:
        parse.nlp
    except AttributeError:
        parse.nlp = spacy.en.English()

    print("attributes logger name=" + logger.name)
    # try:
    #     parse.logger
    # except AttributeError:
    #     import sys
    #     from os.path import dirname, abspath
    #     sys.path.insert(0, dirname(dirname(abspath(__file__))))
    #     import config
    #     parse.logger = config.get_logger()

    doc = parse.nlp(question)
    result = Attributes()
    try:
        result.location = attribute_utils.get_attribute_location_spacy(doc)
        result.named_entity = attribute_utils.get_attribute_named_entity(question)
        result.time = attribute_utils.get_attribute_time_spacy(doc, question)
        result.action = attribute_utils.get_attribute_action(doc)
        result.product = attribute_utils.get_attribute_product(question)
    except KeyError as e:
        # parse.
        logger.error("KeyError. Json config doesn't contain such key:", str(e))
        raise e
    except psycopg2.OperationalError as e:
        # parse.
        logger.error("Error during database operation:\n", str(e))
        raise e
    return Question(
        question=question,
        question_type=attribute_utils.get_question_type(question, result.action),
        answer_type=attribute_utils.get_answer_type(question),
        attributes=result
    )
