ATTRIBUTES = {
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

    "named_entity": [
        "Microsoft",
        "Xamarin"
    ]
}


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


def get_attribute_product(question):
    return get_attribute_by_list(ATTRIBUTES["product"], question.lower())


def get_attribute_named_entity(question):
    return get_attribute_by_list(ATTRIBUTES["named_entity"], question)


def get_attribute_by_list(attr_list, question):
    for word in attr_list:
        if word in question:
            return get_repr(word)


def get_repr(word):
    for repr in SINONYMS:
        if word in SINONYMS[repr]:
            return repr
