
from flask.blueprints import Blueprint
from app import bbs_app

# users_app = Blueprint('users_app', __name__)

@bbs_app.route('/users', methods=['GET'])
def users_index():
    return 'user hello'	


