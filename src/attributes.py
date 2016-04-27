#!/usr/bin/env python3
import spacy.en
from spacy.parts_of_speech import VERB
from datetime import date

from enum import Enum
from model import Question, QuestionType, AnswerType, ActionAttribute, LocationAttribute, TimeAttribute, Attributes
import nltk, re, pprint

ATTRIBUTES_LIST = [
    "country",
    "product",
    "year",
    "named_entity",
    "action"
]

PLURAL = {
    "was": "were",
    "were": "were",
    "is": "are",
    "are": "are",
    "has been": "have been",
    "have been": "have been"
}

ATTRIBUTES = {
    # place
    "country": ["russia", "japan", "germany"],
    "product": [
        "intellij",
        "pycharm",
        "appcode",
        "rubymine",
        "resharper",
        "phpstorm",
        "webstorm",
        "clion",
        "datagrip",
        "resharpercpp",
        "dottrace",
        "dotcover",
        "dotmemory",
        "dotpeek",
        "teamcity",
        "youtrack",
        "upsource",
        "hub",
        "mps"
    ],
    "year": [],
    "named_entity": ["Microsoft", "JetBrains"],
    "action": ["released", "bought"],
    "extra action": ["were", "was", "are", "is"]
}

NEGATIVES = [
    "except",
    "not",
    "outside",
    "without"
]

SINONYMS = {
    "IntellIjidea": ["idea", "intellij idea", "intellijidea"],
    "PyCharm": ["pycharm"],
    "AppCode": ["appcode"],
    "RubyMine": ["rubymine"],
    "ReSharper": ["resharper"],
    "PhpStorm": ["phpstorm"],
    "WebStorm": ["webstorm"],
    "CLion": ["clion"],
    "DataGrip": ["datagrip"],
    "ReSharperCpp": ["resharpercpp"],
    "dotTrace": ["dottrace"],
    "dotCover": ["dotcover"],
    "dotMemory": ["dotmemory"],
    "dotPeek": ["dotpeek"],
    "TeamCity": ["teamcity"],
    "YouTrack": ["youtrack"],
    "Upsource": ["upsource"],
    "Hub": ["hub"],
    "MPS": ["mps"],
    "Russia": ["russia", "russian federation"],
    "Japan": ["japan", "land of the rising sun"],
    "Germany": ["germany", "federal republic of germany"],
}

TYPES = {
    "interrogative": {
        "how many": AnswerType.NUMBER,
        "how much": AnswerType.NUMBER,
        "what": AnswerType.NUMBER,
        "when": AnswerType.DATE
    },

    "qualifier_words": {
        "download": QuestionType.DOWNLOADS,
        "customer": QuestionType.CUSTOMERS,
        "revenue": QuestionType.SALES,
    },

    "action_words": {
        "download": QuestionType.DOWNLOADS,
        "buy": QuestionType.SALES,
        "sell": QuestionType.SALES,
        "release": QuestionType.EVENTS
    }
}

nlp = spacy.en.English()


def parse(question):  # returns a list of question's attributes
    # question is a string
    # doc is spacy-parsed question
    doc = nlp(question)
    result = Attributes()
    result.location = get_attribute_location_spacy(doc)
    result.named_entity = get_attribute_named_entity(question)
    result.time = get_attribute_time_spacy(doc, question)
    result.action = get_attribute_action(doc)
    result.product = get_attribute_product(question)
    return Question(
        question=question,
        question_type=get_question_type(question, get_attribute_action_lemma(doc)),
        answer_type=get_answer_type(question),
        attributes=result
    )


def get_attribute_action_without_synonims(question):
    main_action = get_attribute_by_list_without_sinonyms(ATTRIBUTES["action"], question)
    extra_action = get_attribute_by_list_without_sinonyms(ATTRIBUTES["extra action"], question)
    if extra_action is None:
        return main_action
    elif main_action is None:
        return extra_action
    else:
        return extra_action + " " + main_action


def get_attribute_by_list_without_sinonyms(attr_list, question):
    for word in attr_list:
        if word in question:
            return word

def get_attribute_action_lemma(doc):
    action = None
    others = []
    for token in doc:
        if token.head is token:
            action = token.lemma_
        elif token.pos is VERB:
            others.append(token.lemma_)
    return ActionAttribute(action=action, other=others)


def get_attribute_action(doc):
    action = []
    others = []
    auxiliary = []
    for token in doc:
        if token.head is token:
            action = [token.orth_]
        elif token.pos is VERB and (token.dep_ == "aux" or token.dep_ == "auxpass"):
            auxiliary.append(token.orth_)
        elif token.pos is VERB:
            others.append(token.orth_)
    if action == ["been"]:
        action = auxiliary + action
        auxiliary = []
    return ActionAttribute(action=" ".join(action), other=others, auxiliary=" ".join(auxiliary))

def _get_by_location(location):
    # TODO: call the DB containing countries
    return []


def get_attribute_location_spacy(doc):
    exceptions = []
    candidates = []
    locations = []
    # TODO: to use feature-extraction to determine negative/positive
    for ne in doc.ents:
        if ne.label_ == 'GPE':
            if ne.root.lower_ in NEGATIVES:
                exceptions.append(ne.orth_)
            else:
                candidates.append(ne.orth_)
        elif ne.label_ == 'LOC':
            gpe_list = _get_by_location(ne.orth_)
            if ne.root.lower_ in NEGATIVES:
                exceptions.extend(gpe_list)
            else:
                locations.append(ne.orth_)
                candidates.extend(gpe_list)
    country_list = [x for x in candidates if x not in exceptions]
    result = LocationAttribute(loc_list=locations, countries=country_list)
    return result


def get_attribute_action_simple(question):
    return get_attribute_by_list(ATTRIBUTES["action"], question)


def get_attribute_named_entity(question):
    return get_attribute_by_list(ATTRIBUTES["named_entity"], question)


def _get_gpe(ne_question):
    if isinstance(ne_question, nltk.tree.Tree):
        if ne_question._label is not None and ne_question._label == 'GPE':
            return [x for x in ne_question]
        result = []
        for child in ne_question:
            result.extend(_get_gpe(child))
        return result
    return []


# question is a string here
def get_attribute_location_simple(question):
    tagged_tokens = nltk.pos_tag(nltk.word_tokenize(question))
    ne_question = nltk.ne_chunk(tagged_tokens)
    gpe_list = _get_gpe(ne_question)
    places = []
    for gpe in gpe_list:
        places.append(gpe[0])
    return LocationAttribute(loc_list=gpe_list, countries=places)


def get_attribute_product(question):
    return get_attribute_by_list(ATTRIBUTES["product"], question.lower())


def get_attribute_by_list(attr_list, question):
    for word in attr_list:
        if word in question:
            return get_repr(word)


def get_repr(word):
    for repr in SINONYMS:
        if word in SINONYMS[repr]:
            return repr


def get_attribute_time_spacy(doc, question):
    times = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            times.append(ent)

#    from_data = None
    global prepositions
    global from_date
    global to_date
    global except_date
    global except_prepositions
    except_prepositions = []
    prepositions = []
    except_date = []
    from_date = None
    to_date = None
    for time in times:
        if "ago" in time.orth_:
            cur_year = date.today().year
            count_years = find_number(time.orth_)
            from_date = cur_year - count_years
            to_date = cur_year - count_years
            prepositions = ["in"]
            break
        if "between" in time.orth_:
            part1 = time.orth_.split("and")[0]
            part2 = time.orth_.split("and")[1]
            from_date = find_number(part1)
            to_date = find_number(part2)
            prepositions = ["between"]
            continue
        preposition = time.root.head
        if preposition.orth_ == "since":
            from_date = find_number(time.orth_)
            to_date = None
            prepositions = ["since"]
        elif preposition.orth_ == "from":
            prepositions = ["from"]
            if "to" in time.orth_:
                prepositions.append("to")
            elif "until" in time.orth_:
                prepositions.append("until")
            elif "till" in time.orth_:
                prepositions.append("till")
            if len(prepositions) > 1:
#                print(prepositions)
                part1 = time.orth_.split(prepositions[1])[0]
                part2 = time.orth_.split(prepositions[1])[1]
#                print(part1)
#                print(part2)
                from_date = find_number(part1)
                to_date = find_number(part2)
            from_date = find_number(time.orth_)
        elif preposition.orth_ == "to" or preposition.orth_ == "till" or preposition.orth_ == "until":
            prepositions.append(preposition.orth_)
            to_date = find_number(time.orth_)
        elif preposition.orth_ == "after" or preposition.orth_ == "by":
            from_date = find_number(time.orth_)
            to_date = None
            prepositions = ["after"]
        elif preposition.orth_ == "before":
            from_date = None
            to_date = find_number(time.orth_)
            prepositions = ["before"]
        elif preposition.orth_ == "in" or preposition.orth_ == "within":
            from_date = find_number(time.orth_)
            to_date = find_number(time.orth_)
            prepositions = [preposition.orth_]
        elif preposition.orth_ == "except":
            except_date.append(find_number(time.orth_))
            except_prepositions.append(preposition.orth_)

    print(from_date, to_date, prepositions, except_date, except_prepositions)
    return TimeAttribute(from_date, to_date, prepositions, except_date, except_prepositions)


def find_number(text):
    search_result = re.search('\d+', text)
    if search_result is not None:
        return int(search_result.group(0))
    else:
        return None


def get_attribute_time(question):
    search_result = re.search('in (\d+)', question)
    if search_result is not None:
        time = search_result.group(1)
        return TimeAttribute(start=time, end=time)
    else:
        return TimeAttribute()


def get_question_type(question, action):
    action_type = get_question_type_by_action(action)
    if action_type is not None:
        return action_type
    for word, q_type in TYPES["qualifier_words"].items():
        if word in question:
            return q_type


def get_question_type_by_action(action):
    q_words = TYPES["action_words"]
    if action.main_action in q_words.keys():
        return q_words[action.main_action]


def get_answer_type(question):
    for word, ans_type in TYPES["interrogative"].items():
        if word in question.lower():
            return ans_type
