from flask import Flask
from flask.ext.session import Session
# sess = Session()
bbs_app = Flask(__name__)
bbs_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# sess.init_app(bbs_app)
import views, users
# bbs_app.register_blueprint(users_app, url_prefix='/users')
# bbs_app.register_blueprint(views_app)


