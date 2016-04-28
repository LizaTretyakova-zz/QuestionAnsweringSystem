import psycopg2
from geopy import Nominatim
from base_wrapper import USER, PASSWORD
from model import LocationAttribute
import nltk

REGIONS = {
    'World': 29489,
    'Arab World': 29490,
    'Central Europe and the Baltics': 29491,
    'Caribbean small states': 29492,
    'East Asia & Pacific': 29493,
    'Europe & Central Asia': 29494,
    'Euro area': 29495,
    'European Union': 29496,
    'Fragile and conflict affected situations': 29497,
    'Latin America & Caribbean': 29498,
    'Least developed countries: UN classification': 29499,
    'Middle East & North Africa': 29500,
    'North America': 29501,
    'OECD': 29502,
    'Other small states': 29503,
    'Pacific island small states': 29504,
    'South Asia': 29505,
    'Sub-Saharan Africa': 29506,
    'Small states': 29507,
    'St. Martin (French part)': 29508,
    'Sint Maarten (Dutch part)': 29509,
    'South Sudan': 29510,
    'British Overseas Territories': 29512,
    'Realm of New Zealand': 29513,
    'APAC': 29514,
    'EMEA': 29516
}


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


DEFAULT_REGION = 'World'
INVALID_REGION_ID = 0


def _get_location_id(location):
    result = []
    for region, id in REGIONS.items():
        region_low_list = [x.strip() for x in region.lower().split('&')]
        if len(region_low_list) == 1:
            region_low_list = region_low_list[0]
        location_low = location.lower()
        if location_low in region_low_list:
            result.append(id)
    if not result:
        result.append(INVALID_REGION_ID)
    return result


def _get_by_location(parent_location, target_type):
    parent_location_id = _get_location_id(parent_location)
    query = ("SELECT locations.name\n"
             "FROM locations\n"
             "INNER JOIN location_relations\n"
             "ON locations.id=location_relations.region_id\n"
             "WHERE parent_region_id IN %s\n"
             "AND type=%s")
    conn = psycopg2.connect(database="postgres", user=USER, password=PASSWORD, host="localhost")
    cur = conn.cursor()
    cur.execute(query, (tuple(parent_location_id), target_type))
    res = [x[0] for x in cur.fetchall()]
    print(res)

    return res


def get_attribute_location_spacy(doc):
    country_exceptions = []
    country_candidates = []
    city_exceptions = []
    city_candidates = []
    locations = []  # better to say "regions" -- continents and administrative

    geolocator = Nominatim()

    for ne in doc.ents:
        exceptions = []
        candidates = []
        geocoder = geolocator.geocode(ne.orth_)

        if ne.label_ not in ['GPE', 'LOC', 'ORG'] or not geocoder:
            continue

        if ne.label_ == 'LOC' or ne.label_ == 'ORG':
            # geocoder = geolocator.geocode(ne.orth_)
            gpe_list = _get_by_location(ne.orth_, RegionType['COUNTRY'])
            if ne.root.lower_ in NEGATIVES:
                country_exceptions.extend(gpe_list)
            else:
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

    country_list = [x for x in country_candidates if x not in country_exceptions]
    city_list = [x for x in city_candidates if x not in city_exceptions]
    result = LocationAttribute(locations=locations, countries=country_list, cities=city_list)
    return result


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
