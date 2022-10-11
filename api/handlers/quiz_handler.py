from api import constants

from api.constants import HTTPCodes, APICodes
from api.utils import utils, decorators
from api.Quiz.quiz_types import QuizType
from api.Quiz.generic_quiz import generic_quiz
from api.utils.logger.logger import Logger
from api.utils.sql.interface import Interface

from flask_restful import request

# TODO: Make quiz stuff functional again lol

valid_quiz_options = [QuizType.generic, QuizType.specific]

logger = Logger()


class QuizHandler:

    @staticmethod
    @constants.APP.route("/quiz/<string:quiz_type>/", methods=["POST"])
    @decorators.require_token
    def post(quiz_type: str):
        logger.info(f"[IP: {request.remote_addr}] Received post on route: /quiz/{quiz_type}/")

        data: dict = request.json

        if data is None or data.get("quiz_key") is None or utils.get_name_from_key(data.get("quiz_key").strip()) is None:
            logger.info(f"[IP: {request.remote_addr}] Invalid quiz key has been sent!")
            return utils.give_response({"code": APICodes.INVALID_QUIZ_KEY}, HTTPCodes.OK)

        added_by = utils.get_name_from_key(data.get("quiz_key"))

        quiz_obj: dict = data.get("quiz")

        if quiz_obj is None:
            logger.info(f"[IP: {request.remote_addr}] No quiz has been provided!")
            return utils.give_response({"code": APICodes.NO_QUIZ_PROVIDED}, HTTPCodes.OK)

        if quiz_type == QuizType.generic:
            question = quiz_obj.get("question")
            answer = quiz_obj.get("correct_answer")
            wrong_answers: list[str] = quiz_obj.get("wrong_answers")

            if None in [question, answer, wrong_answers] or len(wrong_answers) != 3:
                return utils.give_response({"code": APICodes.NO_QUIZ_PROVIDED}, HTTPCodes.OK)

            sql = "insert into simple_quizzes (question, possible_answers, correct_answer, added_by) VALUES (%(question)s, %(possible_answers)s, %(correct_answer)s, %(added_by)s)"
            values = {
                "question": question,
                "correct_answer": answer,
                "possible_answers": str(wrong_answers),
                "added_by": added_by
            }

            interface = Interface()

            interface.execute(sql, values)
            interface.close()

            logger.info(f"[IP: {request.remote_addr}] {added_by} has added quiz: {quiz_obj=}")

            return utils.give_response({"code": APICodes.SUCCESS}, HTTPCodes.OK)

        elif quiz_type == QuizType.specific:
            return utils.give_response({"code": APICodes.NOT_IMPLEMENTED_YET}, HTTPCodes.OK)

        else:
            return utils.give_response({"code": APICodes.INVALID_QUIZ_REQUESTED}, HTTPCodes.OK)

    @staticmethod
    @constants.APP.route("/quiz/<string:quiz_type>/", methods=["GET"])
    @decorators.require_token
    def get(quiz_type: str):
        logger.info(f"[IP: {request.remote_addr}] Received get on route: /quiz/{quiz_type}/")

        if quiz_type not in valid_quiz_options:
            return utils.give_response({"code": APICodes.INVALID_QUIZ_REQUESTED}, HTTPCodes.OK)

        quiz = generic_quiz.get_quiz()

        return {"code": APICodes.SUCCESS, "quiz": quiz.return_json()}, HTTPCodes.OK
