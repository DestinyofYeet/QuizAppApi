import json

from flask import Response

from api.Quiz.quiz_types import QuizType
from api.Quiz.generic_quiz.generic_quiz import Quiz
from api.utils.sql.interface import Interface
from api.utils.logger.logger import Logger

import random
import string

logger = Logger()


def get_random_quiz(q_type: QuizType, excluded_ids: list = None) -> Quiz:
    interface = Interface()

    if excluded_ids is None:
        result = interface.execute("select * from quizzes where type = %s ", (q_type,))
    else:
        sql_string = ""
        for excluded_id in excluded_ids:
            sql_string = sql_string + " and id <> %s"
        result = interface.execute(f"select * from quizzes where type = %s {sql_string}", (q_type, *excluded_ids))

    random_quiz = random.choice(result)
    interface.close()
    return Quiz(*random_quiz)


def get_name_from_key(secret):
    with open("data/keys.json") as f:
        data: dict = json.load(f)
    return data.get(secret)


def insert_generic_quiz(question, correct_answer, possible_answer, added_by):
    interface = Interface()

    interface.execute("insert into quizzes (question, possible_answers, correct_answer, type, added_by) values (%s, %s, %s, %s, %s)", (question, possible_answer, correct_answer, "generic", added_by))

    interface.close()


def gen_secret(length: int) -> str:
    secret = ""

    for i in range(length):
        secret += random.choice(random.choice([string.digits, string.ascii_letters, string.punctuation]))

    return secret


def give_response(resp: dict, status: int) -> Response:
    return Response(json.dumps(resp).encode(), status=status, content_type="application/json")


def check_if_token_is_valid(token: str) -> bool:
    interface = Interface()
    sql = "select * from tokens where token=%(token)s"
    result = interface.execute(sql, {"token": token})

    if result is None or len(result) == 0:
        return False

    return True
