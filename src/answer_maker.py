from model import AnswerType, QuestionType
from attributes import TYPES
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


def get_answer(query, answer):
    if query.attributes.location is not None:
        country = query.attributes.location
    if query.question_type is QuestionType.DOWNLOADS:
        return ("There" + xstr(query.attributes.action.main_action, " ", " ") + str(answer) + " downloads" + country_str(query.attributes.location.countries) +
                xstr(query.attributes.time.start, " in "))
    if query.question_type is QuestionType.CUSTOMERS:
        return ("There" + xstr(query.attributes.action.main_action, " ", " ") + str(answer) + " customers " + country_str(query.attributes.location.countries) + " " +
                xstr(query.attributes.time.start, " in "))


# deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type
