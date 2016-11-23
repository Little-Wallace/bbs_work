from functools import wraps
import json
from flask import g, session, request, make_response, Response
from flask.blueprints import Blueprint
from flask import render_template, redirect
from app import bbs_app
from models import User, Group, Message

# views_app = Blueprint('views_app', __name__)

def login_required(func):
    @wraps(func)
    def _decorator(*args, **kwargs):
        if session.has_key('logged_in'):
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return _decorator

@bbs_app.before_request
def load_user():
    if session.has_key('user_id') and session['user_id']:
        user = User.getById(int(session['user_id']))
        print type(user)
        print user
        g.user = user

@bbs_app.route('/login/', methods=['POST'])
def login_post():
    print "here"
    print request.method
    if request.method == 'POST':
        print request.form
        user = User.check(request.form.get('username', None), request.form.get('password', None))
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        print session
        if user:
            print "True"
            session['logged_in'] = True
            session['user_id'] = user.id
            resp.data = json.dumps({'code':0})
            g.user = user
            print g.user.id
            print resp
            return resp
        else:
            resp.data = json.dumps({'code': -1, 'reason': 'password or username wrong'})
        return resp
    return redirect('/')

@bbs_app.route('/', methods=['GET'])
def index():
    if hasattr(g, 'user') and g.user:
        print "login"
        print g.user.__dict__
        return render_template('index.html', user=g.user)
    else:
        print "no login"
        return render_template('base.html')

@bbs_app.route('/classinfo/', methods=['GET'])
@login_required
def group_info():
    cl = Group.getById(g.user.id)
    print '============================='
    return render_template('class.html', user=g.user, group=cl);

@bbs_app.route('/letter/', methods=['GET'])
@login_required
def message_list():
    messages = Letter.getByUserId(g.user.id)
    if messages and len(messages) > 0:
        return render_template('letter.html', user=g.user, messages=messages);
    else:
        return render_template('letter.html', user=g.user)

@bbs_app.route('/homework/', methods=['GET'])
@login_required
def homework_list():
    works = Homework.getByUserId(g.user.id)
    if works and len(works) > 0:
        return render_template('homework.html', user=g.user, works=works);
    else:
        return render_template('homework.html', user=g.user)

