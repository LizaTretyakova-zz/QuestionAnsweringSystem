from model import AnswerType, QuestionType
from attributes import TYPES
from database_wrappers import DownloadsWrapper

def get_answer(question):
    if question.question_type == QuestionType.DOWNLOADS:
        return DownloadsWrapper(question).get()


# deprecated :)
def _get_type(type, question):
    for word, res_type in TYPES[type].items():
        if word in question:
            return res_type
