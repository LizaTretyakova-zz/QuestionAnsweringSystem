#!/usr/bin/env python3
import spacy.en
from spacy.parts_of_speech import VERB
from datetime import date
from geopy.geocoders import Nominatim
from model import Question, QuestionType, AnswerType, ActionAttribute, LocationAttribute, TimeAttribute, Attributes
import nltk, re

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
        question_type=get_question_type(question, result.action),
        answer_type=get_answer_type(question),
        attributes=result
    )


def get_attribute_action(doc):
    action_lemma = None
    action = []
    others = []
    auxiliary = []
    for token in doc:
        if token.head is token:
            action_lemma = token.lemma_
            action = [token.orth_]
        elif token.pos is VERB and (token.dep_ == "aux" or token.dep_ == "auxpass"):
            auxiliary.append(token.orth_)
        elif token.pos is VERB:
            others.append(token.orth_)
    return ActionAttribute(action_lemma=action_lemma, action=" ".join(action), other=others, auxiliary=" ".join(auxiliary))

def _get_by_location(location):
    # TODO: call the DB containing countries
    return []


def get_attribute_location_spacy(doc):
    country_exceptions = []
    country_candidates = []
    city_exceptions = []
    city_candidates = []
    locations = [] # better to say "regions" -- continents and administrative

    geolocator = Nominatim()

    for ne in doc.ents:
        if ne.label_ not in ['GPE', 'LOC']:
            continue

        if ne.label_ is 'LOC':
            gpe_list = _get_by_location(ne.orth_)
            if ne.root.lower_ in NEGATIVES:
                country_exceptions.extend(gpe_list)
            else:
                locations.append(ne.orth_)
                country_candidates.extend(gpe_list)
            continue

        # otherwise
        # it is either a city (type='city' & label='GPE')
        #           or a country (type='administrative' & label='GPE')
        exceptions = []
        candidates = []
        type = geolocator.geocode(ne.orth_).raw['type']
        if type == 'city':
            exceptions = city_exceptions
            candidates = city_candidates
        elif type == 'administrative':
            exceptions = country_exceptions
            candidates = country_candidates
        else:
            print('TYPE:')
            print(type)
            print('city')
            print('administrative')
        # although we separate the results, the processing is similar for both
        if ne.root.lower_ in NEGATIVES:
            exceptions.append(ne.orth_)
        else:
            candidates.append(ne.orth_)

    country_list = [x for x in country_candidates if x not in country_exceptions]
    city_list = [x for x in city_candidates if x not in city_exceptions]
    result = LocationAttribute(locations=locations, countries=country_list, cities = city_list)
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
    return LocationAttribute(locations=gpe_list, countries=places)


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
    propositions = []
    global from_data;
    from_data = None
    for time in times:
        if "ago" in time.orth_:
            cur_year = date.today().year
            count_years = find_number(time.orth_)
            return TimeAttribute(cur_year - count_years, cur_year - count_years, ["in"]                                    )
        if "between" in time.orth_:
            part1 = time.orth_.split("and")[0]
            part2 = time.orth_.split("and")[1]
            return TimeAttribute(find_number(part1), find_number(part2), ["between"])
        proposition = time.root.head
        if proposition.orth_ == "since":
            return TimeAttribute(time.orth_, None, ["since"])
        elif proposition.orth_ == "from":
            propositions.append("from")
            if "to" in time.orth_:
                propositions.append("to")
            elif "until" in time.orth_:
                propositions.append("until")
            elif "till" in time.orth_:
                propositions.append("till")
            if len(propositions) > 1:
                part1 = time.orth_.split(propositions[1])[0]
                part2 = time.orth_.split(propositions[1])[1]
                return TimeAttribute(find_number(part1), find_number(part2), propositions)
            from_data = find_number(time.orth_)
        elif proposition.orth_ == "to" or proposition.orth_ == "till" or proposition.orth_ == "until":
            proposition.append(proposition.orth_)
            return TimeAttribute(from_data, find_number(time.orth_), propositions)
        elif proposition.orth_ == "after" or proposition.orth_ == "by":
            return TimeAttribute(find_number(time.orth_), None, ["after"])
        elif proposition.orth_ == "before":
            return TimeAttribute(None, find_number(time.orth_), ["before"])
        return TimeAttribute(find_number(time.orth_), find_number(time.orth_), ["in"])
    return TimeAttribute(from_data, None, propositions)


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
    if action.action_lemma in q_words.keys():
        return q_words[action.action_lemma]


def get_answer_type(question):
    for word, ans_type in TYPES["interrogative"].items():
        if word in question.lower():
            return ans_type
