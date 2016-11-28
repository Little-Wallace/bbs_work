from flask import Flask
from flask.ext.session import Session
from flask.ext.bootstrap import Bootstrap

# sess = Session()
bbs_app = Flask(__name__)
bbs_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
bootstrap = Bootstrap(bbs_app)
# sess.init_app(bbs_app)
import views
import chart

