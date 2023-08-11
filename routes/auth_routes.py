from flask import Blueprint


from controllers import auth_controller

auth = Blueprint('auth', __name__)


@auth.route('/user/auth', methods=["POST"])
def add_auth_token():
    return auth_controller.auth_token_add()
