from model import QuestionType


TYPES = {
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
