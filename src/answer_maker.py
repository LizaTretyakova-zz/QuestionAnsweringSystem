from model import AnswerType, QuestionType
from attributes import TYPES, PLURAL
from database_wrappers import DownloadsWrapper

past_verbs = ["was", "were"]
present_verbs = ["is", "ara"]


def xstr(smth, prefix = "", suffix = ""):
    if smth is None:
        return ""
    else:
        return prefix + str(smth) + suffix


def country_str(countries):
    result = ""
    for country in countries:
        if result is "":
            result += " in " + country
        else:
            result += " and " + country
    return result


def plural(verb):
    if verb in PLURAL:
        return PLURAL[verb]
    else:
        return verb


def get_answer(query, answer):
    verb = None
    if query.attributes.location is not None:
        countries = query.attributes.location.countries
    else:
        countries = None

    if query.attributes.action.auxiliary is None:
        verb = " ".join(query.attributes.action.main_action)
    else:
        verb = query.attributes.action.auxiliary
    if query.question_type is QuestionType.DOWNLOADS:
        if verb in PLURAL:
            return ("There" + xstr(plural(verb), " ", " ") + str(answer) + " downloads" + country_str(countries) +
                xstr(query.attributes.time.start, " in "))
        else:
            return "Clients" + xstr(verb, " ", " ") + str(answer) + country_str(countries) + "times"
    if query.question_type is QuestionType.CUSTOMERS:
        return ("There" + xstr(plural(verb), " ", " ") + str(answer) + " customers" + country_str(countries) +
                xstr(query.attributes.time.start, " in "))


# deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type
