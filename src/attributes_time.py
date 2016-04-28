from model import TimeAttribute
from datetime import date
import re


def get_attribute_time_spacy(doc, question):
    times = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            times.append(ent)

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
                part1 = time.orth_.split(prepositions[1])[0]
                part2 = time.orth_.split(prepositions[1])[1]
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
