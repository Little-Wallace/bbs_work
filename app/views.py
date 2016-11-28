from functools import wraps
import json
from flask import g, session, request, make_response, Response, url_for
from flask.blueprints import Blueprint
from flask import render_template, redirect
from app import bbs_app
from models import User, Topic, Message
from models import session as sess

# views_app = Blueprint('views_app', __name__)

def login_required(func):
    @wraps(func)
    def _decorator(*args, **kwargs):
        if session.has_key('logged_in') and session['logged_in'] == True:
            return func(*args, **kwargs)
        else:
            return redirect('/login/')
    return _decorator

@bbs_app.before_request
def load_user():
    if not session.has_key('user_id'):
        return
    if session['user_id']:
        #print session['user_id']
        user = User.getById(int(session['user_id']))
        if user:
           # print type(user)
           # print user
            g.user = user

@bbs_app.route('/logincc/', methods=['POST'])
def login_post():
    #print "here"
    #print request.method
    if request.method == 'POST':
       # print request.form
        user = User.check(request.form.get('username', None), request.form.get('password', None))
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #print session
        if user:
           # print "True"
            session['logged_in'] = True
            session['user_id'] = user.id
            resp.data = json.dumps({'code':0})
            g.user = user
           # print g.user.id
           # print resp
            return resp
        else:
            resp.data = json.dumps({'code': -1, 'reason': 'password or username wrong'})
        return resp
    return redirect('/')

@bbs_app.route('/haha', methods=['GET'])
def index_liuwei():
   # print url_for('static', filename='js/Data.js')
    if hasattr(g, 'user') and g.user:
       # print "login"
       # print g.user.__dict__
        return render_template('index.html', user=g.user)
    else:
       # print "no login"
        return redirect('/login/')

@bbs_app.route('/message/list/', methods=['GET'])
@login_required
def message_list():
    messages = Message.getByUserId(g.user.id)
    if messages and len(messages) > 0:
        return render_template('message.html', user=g.user, messages=messages);
    else:
        return render_template('message.html', user=g.user)

@bbs_app.route('/message/<int:m_id>/', methods=['GET'])
@login_required
def message_info(m_id):
    m = Message.getById(m_id)
    if not m:
        return render_template('error.html', user=g.user, error='haha')
    if m.user_id != g.user.id:
        return render_template('error.html', user=g.user, error='xixi')
    m.status = u'haha'
    return render_template('message_content.html', user=g.user, message=m)

@bbs_app.route('/message/add/', methods=['POST'])
@login_required
def addmessage():
    if g.user.identity != User.TEACHER:
        return render_template('error.html', user=g.user, error=u'haha')
    m = Message()
    m.title = request.form.get('title', None)
    m.desc = request.form.get('desc', None)
    m.user_id = request.form.get('user_id', None)
    m.author = g.user.name
    m.status = u'haha'
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    try:
        sess.add(m)
        sess.commit()
        resp.data = json.dumps({'code':0})
    except Exception, ex:
        resp.data = json.dumps({'code': -1, 'reason': ex})
    return resp

@bbs_app.route('/homework/', methods=['GET'])
@login_required
def homework_list():
    works = Homework.getByUserId(g.user.id)
    if works and len(works) > 0:
        return render_template('homework.html', user=g.user, works=works);
    else:
        return render_template('homework.html', user=g.user)




