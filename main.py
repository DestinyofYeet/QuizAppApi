import sys

import waitress

from api.utils.logger.logger import Logger

logger = Logger(where_to_log_file="logs/")

from api.utils.config.config import Config
from api import constants

from api.handlers import quiz_handler, user_handler, big_quiz_handler


def main():
    config = Config()

    DEBUG = True if "--debug" in sys.argv else False

    quiz_handler.QuizHandler()
    user_handler.UserHandler()
    big_quiz_handler.BigQuizHandler()

    logger.info(f"Running in {'debug' if DEBUG else 'production'} mode, port={config.api_port}, host={config.api_host}")

    if DEBUG:  # use in development
        constants.APP.run(host=config.api_host, port=config.api_port, debug=True)
    else:
        waitress.serve(constants.APP, host=config.api_host, port=config.api_port,
                       url_scheme="https")  # use in production


if __name__ == '__main__':
    main()
