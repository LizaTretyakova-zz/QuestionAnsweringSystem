from src.model import TimeAttribute
from datetime import date
import re


def get_attribute_time_spacy(doc, question):

    times = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            times.append(ent)

    complex_prepositions = []
    except_date = []

    from_date_for_segment = None

    from_date = None
    to_date = None

    time_attribute = TimeAttribute()

    for time in times:
        if "ago" in time.orth_:
            cur_year = date.today().year
            count_years = find_number(time.orth_)
            from_date = cur_year - count_years
            to_date = cur_year - count_years
            time_attribute.add_segment(from_date, to_date, ["in"])
            continue
        if "between" in time.orth_:
            part1 = time.orth_.split("and")[0]
            part2 = time.orth_.split("and")[1]
            from_date = find_number(part1)
            to_date = find_number(part2)
            time_attribute.add_segment(from_date, to_date, ["between", "and"])
            continue
        preposition = time.root.head
        if preposition.orth_ == "since":
            from_date = find_number(time.orth_)
            to_date = None
            time_attribute.add_segment(from_date, None, ["since"])
        elif preposition.orth_ == "from":
            complex_prepositions = ["from"]
            if "to" in time.orth_:
                complex_prepositions.append("to")
            elif "until" in time.orth_:
                complex_prepositions.append("until")
            elif "till" in time.orth_:
                complex_prepositions.append("till")
            if len(complex_prepositions) > 1:
                part1 = time.orth_.split(complex_prepositions[1])[0]
                part2 = time.orth_.split(complex_prepositions[1])[1]
                from_date = find_number(part1)
                to_date = find_number(part2)
                time_attribute.add_segment(from_date, to_date, complex_prepositions)
                complex_prepositions = []
                continue
            from_date = find_number(time.orth_)
            if from_date_for_segment is not None:
                time_attribute.add_segment(from_date_for_segment, None, complex_prepositions)
            from_date_for_segment = find_number(time.orth_)
        elif preposition.orth_ == "to" or preposition.orth_ == "till" or preposition.orth_ == "until":
            complex_prepositions.append(preposition.orth_)
            to_date = find_number(time.orth_)
            time_attribute.add_segment(from_date_for_segment, to_date, complex_prepositions)
            from_date_for_segment = None
            complex_prepositions = []
        elif preposition.orth_ == "after" or preposition.orth_ == "by":
            from_date = find_number(time.orth_)
            to_date = None
            time_attribute.add_segment(from_date, None, [preposition.orth_])
        elif preposition.orth_ == "before":
            from_date = None
            to_date = find_number(time.orth_)
            time_attribute.add_segment(None, to_date, ["before"])
        elif preposition.orth_ == "in" or preposition.orth_ == "within" or preposition.orth_ == "during":
            from_date = find_number(time.orth_)
            to_date = find_number(time.orth_)
            time_attribute.add_segment(from_date, to_date, [preposition.orth_])
        elif preposition.orth_ == "except" or preposition.orth_ == "without":
            except_value = find_number(time.orth_)
            except_date.append(except_value)
            time_attribute.add_except_segment(except_value, except_value, [preposition.orth_])

    find_another_dates(doc, time_attribute)

    time_attribute.eval_real_segments()

    time_attribute.from_date = from_date
    time_attribute.to_date = to_date
    time_attribute.except_date = except_date

    print(time_attribute.real_segments)

    return time_attribute


def find_another_dates(doc, time_attribute):
    from_date_for_segment = None
    for token in doc:
        if token.is_digit:
            cur_token = token
            count_steps = 0
            while cur_token.head is not cur_token and cur_token.dep_ == "conj":
                cur_token = cur_token.head
                count_steps += 1
            cur_token = cur_token.head
            if cur_token.orth_ == "in" or cur_token.orth_ == "within" or cur_token.orth_ == "during" \
                    and count_steps != 0:
                time_attribute.add_segment(find_number(token.orth_), find_number(token.orth_), [cur_token.orth_])
            if cur_token.orth_ == "without" or cur_token.orth_ == "except" and count_steps != 0:
                time_attribute.add_except_segment(find_number(token.orth_), find_number(token.orth_), [cur_token.orth_])
            if cur_token.orth_ == "from":
                if from_date_for_segment is not None:
                    time_attribute.add_segment(from_date_for_segment, None, ["from"])
                from_date_for_segment = find_number(token.orth_)
            if cur_token.orth_ == "till":
                if from_date_for_segment is not None:
                    prepositions = ["from", "till"]
                else:
                    prepositions = ["till"]
                time_attribute.add_segment(from_date_for_segment, find_number(token.orth_), prepositions)
                from_date_for_segment = None


def find_number(text):
    search_result = re.search('\d+', text)
    if search_result is not None:
        return int(search_result.group(0))
    else:
        return None
