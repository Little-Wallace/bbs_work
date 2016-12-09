from flask import Flask
from flask.ext.session import Session
from flask.ext.bootstrap import Bootstrap
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from models import DBsession

# sess = Session()
bbs_app = Flask(__name__)
bbs_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
bootstrap = Bootstrap(bbs_app)
manager = Manager(bbs_app)
migrate = Migrate(bbs_app, DBsession)
manager.add_command('db', MigrateCommand)
# sess.init_app(bbs_app)
import views
import chart

