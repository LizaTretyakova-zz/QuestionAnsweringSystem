from src.model import QuestionType, Segment

PLURAL = {
    "was": "were",
    "were": "were",
    "is": "are",
    "are": "are",
    "has been": "have been",
    "have been": "have been"
}

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
    result = ""
    is_previous = [False, False]
    previous_preposition = None
    positive_label = ["positive"]
    negative_label = ["negative"]
    label = [positive_label, negative_label]
    for segment in time.segments_for_answer:
        if segment.preposition:
            if len(segment.preposition) == 2:
                if is_previous[segment.preposition_type]:
                    result += " and"
                result += " " + segment.preposition[0] + " " + str(segment.start) + " " + \
                          segment.preposition[1] + " " + str(segment.end)
                is_previous[segment.preposition_type] = True
                previous_preposition = segment.preposition + label[segment.preposition_type]
            else:
                if segment.start is not None:
                    if is_previous[segment.preposition_type]:
                        result += " and"
                    if previous_preposition != segment.preposition + label[segment.preposition_type]:
                        result += " " + segment.preposition[0]
                    result += " " + str(segment.start)
                    is_previous[segment.preposition_type] = True
                    previous_preposition = segment.preposition + label[segment.preposition_type]
                elif segment.end is not None:
                    if is_previous[segment.preposition_type]:
                        result += "and"
                    if previous_preposition != segment.preposition + label[segment.preposition_type]:
                        result += " " + segment.preposition[0]
                    result += " " + str(segment.end)
                    is_previous[segment.preposition_type] = True
                    previous_preposition = segment.preposition + label[segment.preposition_type]
        elif segment.preposition_type == Segment.PrepositionType.positive:
            if segment.start:
                if segment.end:
                    if segment.start != segment.end:
                        if is_previous[segment.preposition_type]:
                            result += " and"
                        result += " between " + str(segment.start) + " and " + str(segment.end)
                        is_previous[segment.preposition_type] = True
                        previous_preposition = ["between", "and"] + positive_label
                    else:
                        if is_previous[segment.preposition_type]:
                            result += " and"
                        if previous_preposition != ["in"] + positive_label:
                            result += " in " + str(segment.start)
                        is_previous[segment.preposition_type] = True
                        previous_preposition = ["in"] + positive_label
                else:
                    if is_previous[segment.preposition_type]:
                        result += " and"
                    result += " since " + str(segment.start)
                    is_previous[segment.preposition_type] = True
                    previous_preposition = ["since"]
            else:
                if segment.end:
                    if is_previous[segment.preposition_type]:
                        result += " and"
                    result += " till " + str(segment.end)
                    is_previous[segment.preposition_type] = True
                    previous_preposition = ["till"]
        elif segment.preposition_type == Segment.PrepositionType.negative:
            if segment.start:
                if segment.end:
                    if segment.start != segment.end:
                        if is_previous[segment.preposition_type]:
                            result += " and"
                        result += " except the dates between " + str(segment.start) + " and " + str(segment.end)
                        is_previous[segment.preposition_type] = True
                        previous_preposition = ["between", "and"] + negative_label
                    else:
                        if is_previous[segment.preposition_type]:
                            result += " and"
                        if previous_preposition != ["without"] + negative_label:
                            result += " without"
                        result += " " + str(segment.start)
                        is_previous[segment.preposition_type] = True
                        previous_preposition = ["without"] + negative_label
                else:
                    if is_previous[segment.preposition_type]:
                        result += " and"
                    result += " except the dates since " + str(segment.start)
                    is_previous[segment.preposition_type] = True
                    previous_preposition = ["since"] + negative_label
            else:
                if segment.end:
                    if is_previous[segment.preposition_type]:
                        result += " and"
                    result += " except the dates till " + str(segment.end)
                    is_previous[segment.preposition_type] = True
                    previous_preposition = ["till"] + negative_label
    return result


def get_answer(query, answer):

    if query.attributes.location is not None:
        countries = query.attributes.location.countries
    else:
        countries = None

    if not query.attributes.action.auxiliary:
        verb = query.attributes.action.action
    else:
        verb = query.attributes.action.auxiliary
    if query.question_type is QuestionType.DOWNLOADS:
        if verb in PLURAL:
            return ("There" + xstr(plural(verb), " ") + " " + str(answer) + " downloads" + country_str(countries) +
                    create_time_part(query.attributes.time))
        else:
            product = query.attributes.product
            return "Clients" + xstr(verb, " ") + " " + product + " " + str(answer) + \
                   country_str(countries) + " times" + create_time_part(query.attributes.time)
    if query.question_type is QuestionType.CUSTOMERS:
        return ("There" + xstr(plural(verb), " ") + " " + str(answer) + " customers" + country_str(countries) +
                create_time_part(query.attributes.time))
