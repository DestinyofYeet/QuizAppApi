from api import constants
from api.constants import HTTPCodes, APICodes
from api.utils.sql.interface import Interface
from api.utils import utils, decorators
from api.utils.logger.logger import Logger

import bcrypt

from flask_restful import request

logger = Logger()


class UserHandler:

    @staticmethod
    @constants.APP.route("/accounts/create", methods=["POST"])
    @decorators.require_username_and_password
    def create_account():
        data: dict = request.json

        provided_username: str = data.get("username")
        provided_password: str = data.get("password")

        interface = Interface()

        # ====================Checks for already existing username=====================

        sql = "select username from users where username=%(name)s"

        result = interface.execute(sql, {"name": provided_username})

        if len(result) != 0:
            logger.info(f"[IP: {request.remote_addr}] Attempted account creation with account name \"{provided_username}\" failed because an account with that name already exists!")
            return utils.give_response({"code": APICodes.ACCOUNT_ALREADY_EXISTS}, HTTPCodes.OK)

        # ==================Creates the database entry=================================

        hashed_pw = bcrypt.hashpw(provided_password.encode(), bcrypt.gensalt())

        sql = "insert into users (username, password) values (%(username)s, %(password)s)"

        interface.execute(sql,
                          {
                              "username": provided_username,
                              "password": hashed_pw.decode()
                          })

        interface.close()

        logger.info(f"[IP: {request.remote_addr}] Created a new account with the name \"{provided_username}\"!")
        return utils.give_response({"code": APICodes.SUCCESS}, HTTPCodes.OK)

    @staticmethod
    @constants.APP.route("/accounts/login", methods=["POST"])
    @decorators.require_username_and_password
    def login_account():
        data: dict = request.json

        interface = Interface()

        provided_username = data.get("username")
        provided_password = data.get("password")

    # ================= Checks if the account exists ==============================================

        sql = "select * from users where username=%(username)s"

        result = interface.execute(sql, {"username": provided_username})

        if len(result) == 0 or result is None:
            logger.info(f"[IP: {request.remote_addr}] Attempted login from user \"{provided_username}\" failed, since there was no account found!")
            return utils.give_response({"code": APICodes.BAD_USERNAME_OR_PASSWORD}, HTTPCodes.OK)

        acc_id, acc_name, hashed_pw, is_enabled = result[0]

        match = bcrypt.checkpw(provided_password.encode(), hashed_pw.encode())

    # ================ Checks if the password is correct ===============================================

        if not match:
            logger.info(f"[IP: {request.remote_addr}] Attempted login from user \"{provided_username}\" failed, since the password was incorrect!")
            return utils.give_response({"code": APICodes.BAD_USERNAME_OR_PASSWORD}, HTTPCodes.OK)

    # ================= Token is being set in the tokens database =====================================

        token = utils.gen_secret(20)

        sql = "select * from tokens where user_id=%(id)s"

        result = interface.execute(sql, {"id": acc_id})

        if result:
            sql = "update tokens set token=%(token)s where user_id=%(id)s"
            interface.execute(sql, {"token": token, "id": acc_id})

        else:
            sql = "insert into tokens (user_id, token) values (%(id)s, %(token)s)"
            interface.execute(sql, {"id": acc_id, "token": token})

        interface.close()

        logger.info(f"[IP: {request.remote_addr}] User \"{provided_username}\" successfully logged in! Got token: {token}")
        return utils.give_response({"token": token, "code": APICodes.SUCCESS}, HTTPCodes.OK)
