from model import AnswerType, QuestionType
from attributes import TYPES, PLURAL
from database_wrappers import DownloadsWrapper

past_verbs = ["was", "were"]
present_verbs = ["is", "ara"]


def xstr(smth, prefix=""):
    if smth is None:
        return ""
    else:
        return prefix + str(smth)


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


def create_time_part(time):
    if time.start is None and time.end is None:
        return ''
    elif time.start is None:
        return " " + " ".join(time.preposition) + " " + str(time.end)
    elif time.end is None:
        return " " + " ".join(time.proposition) + " " + str(time.start)
    elif time.start is not None and time.end is not None and time.end != time.start:
        if len(time.proposition) == 2:
            return " from " + str(time.start) + " to " + str(time.end)
        else:
            return " between " + str(time.start) + " and " + str(time.end)
    else:
        return ' in ' + str(time.start)


def get_answer(query, answer):
    verb = None
    if query.attributes.location is not None:
        countries = query.attributes.location.countries
    else:
        countries = None

    if query.attributes.action.auxiliary is None or query.attributes.action.auxiliary == "":
        verb = query.attributes.action.action
    else:
        verb = query.attributes.action.auxiliary
    if query.question_type is QuestionType.DOWNLOADS:
        if verb in PLURAL:
            return ("There" + xstr(plural(verb), " ") + " " + str(answer) + " downloads" + country_str(countries) +
                    create_time_part(query.attributes.time))
        else:
            return "Clients" + xstr(verb, " ") + " it " + str(answer) + country_str(countries) + " times"
    if query.question_type is QuestionType.CUSTOMERS:
        return ("There" + xstr(plural(verb), " ") + " " + str(answer) + " customers" + country_str(countries) +
                create_time_part(query.attributes.time))


# deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type
