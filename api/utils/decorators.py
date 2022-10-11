func_inner_map = {}

inner_func_reference_map = {}


def require_username_and_password(func):

    parser = f"def root():\n" \
             "  from api.constants import HTTPCodes, APICodes\n" \
             "  from flask import request\n" \
             "  from api.utils import utils\n" \
             "\n" \
             f"  def parse_{len(func_inner_map.keys())}(*args, **kwargs):\n" \
             "    data = request.json\n" \
             "    provided_username = data.get('username')\n" \
             "    provided_password = data.get('password')\n" \
             "    if provided_username is None:\n" \
             "      return utils.give_response({'code': APICodes.NO_PASSWORD_OR_USERNAME_PROVIDED}, HTTPCodes.OK)\n" \
             "    elif provided_password is None:\n" \
             "      return utils.give_response({'code': APICodes.NO_PASSWORD_OR_USERNAME_PROVIDED}, HTTPCodes.OK)\n" \
             "    elif len(provided_username) > 20:\n" \
             "      return utils.give_response({'code': APICodes.MAX_CHAR_LENGTH_EXCEEDED}, HTTPCodes.OK)\n" \
             f"    return inner_func_reference_map['parse_{len(func_inner_map.keys())}'](*args, **kwargs)\n" \
             f"  return parse_{len(func_inner_map.keys())}"
    exec(parser)
    exec(f"func_inner_map['{func.__name__}'] = root()")

    inner_func_reference_map[func_inner_map[func.__name__].__name__] = func

    return func_inner_map[func.__name__]


def require_token(func):
    parser = f"def root():\n" \
             "  from api.constants import HTTPCodes, APICodes\n" \
             "  from flask import request\n" \
             "  from api.utils import utils\n" \
             "\n" \
             f"  def parse_{len(func_inner_map.keys())}(*args, **kwargs):\n" \
             "    headers = request.headers\n" \
             "    token = headers.get('token')\n" \
             "    if token is None or not utils.check_if_token_is_valid(token):\n" \
             "      return utils.give_response({'code': APICodes.NO_TOKEN_PROVIDED}, HTTPCodes.OK)\n" \
             f"    return inner_func_reference_map['parse_{len(func_inner_map.keys())}'](*args, **kwargs)\n" \
             f"  return parse_{len(func_inner_map.keys())}"
    exec(parser)
    exec(f"func_inner_map['{func.__name__}'] = root()")

    inner_func_reference_map[func_inner_map[func.__name__].__name__] = func

    return func_inner_map[func.__name__]
