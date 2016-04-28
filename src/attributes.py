#!/usr/bin/env python3

import spacy.en
from model import Question, Attributes
from attributes_action import get_attribute_action
from attributes_location import get_attribute_location_spacy
from attributes_time import get_attribute_time_spacy
from attributes_answer_type import get_answer_type
from attributes_question_type import get_question_type
from attributes_default_utils import get_attribute_product, get_attribute_named_entity

def parse(question:str)->Question:  # returns a list of question's attributes
    # question is a string
    # doc is spacy-parsed question

    try:
        parse.nlp
    except AttributeError:
        parse.nlp = spacy.en.English()

    doc = parse.nlp(question)
    result = Attributes()
    result.location = get_attribute_location_spacy(doc)
    result.named_entity = get_attribute_named_entity(question)
    result.time = get_attribute_time_spacy(doc, question)
    result.action = get_attribute_action(doc)
    result.product = get_attribute_product(question)
    return Question(
        question=question,
        question_type=get_question_type(question, result.action),
        answer_type=get_answer_type(question),
        attributes=result
    )
