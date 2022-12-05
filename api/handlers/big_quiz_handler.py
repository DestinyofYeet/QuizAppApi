from api import constants
from api.utils import decorators, utils
from api.Quiz.specific_quiz import specific_quiz
from api.utils.sql.interface import Interface


class BigQuizHandler:

    @staticmethod
    @constants.APP.route("/big_quiz/<string:location_name>", methods=['GET'])
    @decorators.require_token
    def get(location_name: str):
        interface = Interface()

        sql = "select punkt_name from quizapp_db.gr_rätsel_punkt"
        result = interface.execute(sql)

        available_locations = [i[0] for i in result]

        if location_name not in available_locations:
            return utils.give_response({"code": constants.APICodes.INVALID_SPECIFIC_LOCATION_NAME,
                                        "error": "Invalid name!"}, constants.HTTPCodes.OK)

        quiz = specific_quiz.get_quiz(location_name)

        return utils.give_response({"code": constants.APICodes.SUCCESS, "quiz": quiz.return_json()}, constants.HTTPCodes.OK)
