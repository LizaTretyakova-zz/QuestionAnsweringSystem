from spacy.parts_of_speech import VERB
from src.model import ActionAttribute


def get_attribute_action(doc)->list:
    action_lemma = None
    action = []
    others = []
    auxiliary = []
    for token in doc:
        if token.head is token:
            action_lemma = token.lemma_
            action = [token.orth_]
        elif token.pos is VERB and (token.dep_ == "aux" or token.dep_ == "auxpass"):
            auxiliary.append(token.orth_)
        elif token.pos is VERB:
            others.append(token.orth_)
    if action == ["been"]:
        action = auxiliary + action
        auxiliary = []
    return ActionAttribute(action_lemma=action_lemma,
                           action=" ".join(action),
                           other=others,
                           auxiliary=" ".join(auxiliary))


def get_attribute_action_simple(question):
    return get_attribute_by_list(ATTRIBUTES["action"], question)

