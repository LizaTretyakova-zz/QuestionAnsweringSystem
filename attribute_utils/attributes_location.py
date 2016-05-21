from geopy import Nominatim
from src.model import LocationAttribute
import database_utils
import nltk
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)

COUNT_ATTEMPTS = 10


NEGATIVES = [
    "except",
    "not",
    "outside",
    "without"
]


RegionType = {
    'COUNTRY': 0,
    'CITY': 1
}


def get_attribute_location_spacy(doc) -> LocationAttribute:
    try:
        get_attribute_location_spacy.location_wrapper
    except AttributeError:
        get_attribute_location_spacy.location_wrapper = database_utils.LocationWrapper()

    country_exceptions = []
    country_candidates = []
    city_exceptions = []
    city_candidates = []
    locations = []  # better to say "regions" -- continents and administrative

    geolocator = Nominatim()

    for ne in doc.ents:
        exceptions = []
        candidates = []
        for i in range(COUNT_ATTEMPTS):
            try:
                geocoder = geolocator.geocode(ne.orth_)
                break
            except:
                if i is COUNT_ATTEMPTS - 1:
                    raise

        if ne.label_ not in ['GPE', 'LOC', 'ORG'] or not geocoder:
            continue

        if ne.label_ == 'LOC' or ne.label_ == 'ORG':
            # geocoder = geolocator.geocode(ne.orth_)
            gpe_list = get_attribute_location_spacy.location_wrapper.get_by_location(ne.orth_, RegionType['COUNTRY'])
            if ne.root.lower_ in NEGATIVES:
                # country_exceptions = ([] if country_exceptions is None else country_exceptions)
                country_exceptions.extend(gpe_list)
            else:
                # locations = ([] if locations is None else locations)
                locations.append(ne.orth_)
                country_candidates.extend(gpe_list)
            continue

        # otherwise
        # it is either a city (type='city' & label='GPE')
        #           or a country (type='administrative' & label='GPE')
        type = geocoder.raw['type']
        if type == 'city':
            exceptions = city_exceptions
            candidates = city_candidates
        elif type == 'administrative':
            exceptions = country_exceptions
            candidates = country_candidates
        else:
            print('TYPE:')
            print('Spacy type: ', ne.label_)
            print('Nominatim type: ', type)
            print('city')
            print('administrative')
        # although we separate the results, the processing is similar for both
        if ne.root.lower_ in NEGATIVES:
            exceptions.append(ne.orth_)
        else:
            candidates.append(ne.orth_)

    if country_candidates == [] \
            and country_exceptions == [] \
            and city_candidates == [] \
            and city_candidates == [] \
            and locations == []:
        return None

    country_list = [x for x in country_candidates if x not in country_exceptions]
    city_list = [x for x in city_candidates if x not in city_exceptions]
    result = LocationAttribute(locations=locations, countries=country_list, cities=city_list)
    logging.debug(result)
    return result


def _get_gpe(ne_question) -> list:
    if isinstance(ne_question, nltk.tree.Tree):
        if ne_question._label is not None and ne_question._label == 'GPE':
            return [x for x in ne_question]
        result = []
        for child in ne_question:
            result.extend(_get_gpe(child))
        return result
    return []


def get_attribute_location_simple(question: str) -> LocationAttribute:
    tagged_tokens = nltk.pos_tag(nltk.word_tokenize(question))
    ne_question = nltk.ne_chunk(tagged_tokens)
    gpe_list = _get_gpe(ne_question)
    places = []
    for gpe in gpe_list:
        places.append(gpe[0])
    return LocationAttribute(locations=gpe_list, countries=places)
