from flask import Flask
bbs_app = Flask(__name__)
import views, users
# bbs_app.register_blueprint(users_app, url_prefix='/users')
# bbs_app.register_blueprint(views_app)


