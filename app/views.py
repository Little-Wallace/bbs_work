import json
from flask import g, session, request, make_response
from flask.blueprints import Blueprint
from flask import render_template, redirect
from app import bbs_app
from models import User

# views_app = Blueprint('views_app', __name__)

def login_require(func):
    def __decorator__():
        if session['logged_in'] == True:
            func()
        else:
            return redirect('/')
    return __decorator__

@bbs_app.route('/login/', methods=['POST'])
def login_post():
    if request.method == 'POST':
        user = User.check(request.form['username'], request.form['password'])
        resp = make_response()
        resp.content_type='text/event-stream'
        if user:
            session['user'] = user
            session['logged_in'] = True
            resp.data = json.dumps({'code':0 })
            g.user = user
            return resp
        else:
            resp.data = json.dumps({'code': -1, 'reason': 'password or username wrong'})
        return resp
    return redirect('/')

@bbs_app.route('/', methods=['GET'])
def index():
    if g.user:
        return render_template('index.html', {'user': user})
    else:
        return render_template('index.html')


