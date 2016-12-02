#encoding: utf-8
from functools import wraps
import json
from flask import g, session, request, make_response, Response, url_for
from flask.blueprints import Blueprint
from flask import render_template, redirect
from flask.ext.wtf import Form
from app import bbs_app
from models import User, Message, Grade, or_, Task
from models import session as sess
from wtforms import StringField, TextAreaField, SubmitField, HiddenField, PasswordField
from wtforms.validators import Required

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

def json_response():
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

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
    q = Message.getByGroupId(g.user.group_id, g.user.id)
    status = -1
    if 'status' in request.args:
        q = q.filter(Message.status==request.args.get('status'))
        status = int(request.args.get('status'))
    if 'desc' in request.args:
        q = q.filter(Message.title.like("%" + request.args.get('desc') + "%"))
    messages = q.order_by(Message.create_time.desc()).all()
    if messages and len(messages) > 0:
        resp = []
        for m in messages:
            res = {}
            res['id'] = m.id
            res['title'] = m.title
            res['author'] = u'无'
            res['create_time'] = str(m.create_time)
            if m.status == 1:
                res['status'] = u'已读'
            else:
                res['status'] = u'未读'
            u = User.getById(m.author_id)
            if u:
                res['author'] = u.name
            resp.append(res)
        return render_template('message_list.html', user=g.user, messages=resp, status=status);
    else:
        return render_template('message_list.html', user=g.user)

@bbs_app.route('/message/<int:m_id>/', methods=['GET'])
@login_required
def message_info(m_id):
    m = Message.getById(m_id)
    if not m:
        return render_template('error.html', user=g.user, error='haha')
    if m.user_id != g.user.id and m.group_id != g.user.group_id and m.author_id != g.user.id:
        return render_template('error.html', user=g.user, error='xixi')
    m.status = 1
    sess.commit()
    return render_template('message.html', user=g.user, m=m)

@bbs_app.route('/message/add/', methods=['POST'])
@login_required
def addmessage():
    if g.user.priv != User.TEACHER:
        return render_template('error.html', user=g.user, error=u'haha')
    m = Message()
    m.title = request.form.get('title', None)
    m.desc = request.form.get('content', None)
    m.user_id = request.form.get('user_id', None)
    group_id = request.form.get('group_id', None)
    m.author_id = g.user.id
    m.status = 0
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    group = User.getByGroupId(group_id)
    try:
        for u in group:
            mm = Message()
            mm.title = m.title
            mm.desc = m.desc
            mm.user_id = u.id
            mm.status = 0
            mm.author_id = g.user.id
            sess.add(mm)
        sess.add(m)
        sess.commit()
        resp.data = json.dumps({'code':0, 'msg': u'发布成功'})
    except Exception, ex:
        resp.data = json.dumps({'code': -1, 'reason': ex})
    return resp


@bbs_app.route('/grade/', methods=['GET'])
@login_required
def grade_list():
    print g.user.priv
    if g.user.priv == 'teacher':
        q = Grade.getByTeacherId(g.user.id)
    else: 
        q = Grade.getByUserId(g.user.id)
    subj = request.args.get('subject', None)
    if subj:
        grades = q.filter(or_(Grade.subject.like("%" + subj + "%"), Grade.name.like("%" + subj + "%"))).all()
    else:
        grades = q.all()
    resp = []
    for grade in grades:
        res = {}
        res['id'] = grade.student_id
        res['teacher'] = u'无'
        res['name'] = u'数据缺失'  
        u = User.getById(grade.student_id)
        if u:
            res['name'] = u.name
        u = User.getById(grade.teacher_id)
        if u:
            res['teacher'] = u.name
        res['subject'] = grade.subject
        res['contest_time'] = str(grade.contest_time)
        res['semester'] = grade.semester
        res['score'] = grade.score
        resp.append(res)
    return render_template('grade.html', user=g.user, grades=resp)

@bbs_app.route('/grade/data/', methods=['POST'])
@login_required
def get_grade_data():
    g_id = request.form.get('student_id')
    subject = request.form.get('subject')
    grades = Grade.getByUserId(g_id).filter(Grade.subject==subject).\
            order_by(Grade.contest_time).all()
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    data = {}
    data_name = []
    data_value = []
    for x in grades:
        data_value.append(x.score)
        data_name.append(str(x.contest_time))
    u = User.getById(g_id)
    data['code'] = 0
    data['value'] = data_value
    data['name'] = data_name
    data['title'] = User.getById(g_id).name + u"的" + subject + u"成绩曲线"
    resp.data = json.dumps(data)
    return resp

@bbs_app.route('/grade/add/', methods=['POST'])
@login_required
def addgrade():
    if g.user.priv != User.TEACHER:
        return render_template('error.html', user=g.user, error=u'haha')
    m = Grade()
    m.title = request.form.get('subject', None)
    m.contest_time = request.form.get('contest_time', None)
    m.user_id = request.form.get('user_id', None)
    m.teacher_id = g.user.id
    m.semester = request.form.get('semester', None)
    m.score = request.form.get('score', None)
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    try:
        sess.add(m)
        sess.commit()
        resp.data = json.dumps({'code':0, 'msg': u'发布成功'})
    except Exception, ex:
        resp.data = json.dumps({'code': -1, 'reason': ex})
    return resp


@bbs_app.route('/homework/list/', methods=['GET'])
@login_required
def homework_list():
    if g.user.priv == 'teacher':
        q = Task.getByTeacherId(g.user.id)
    else:
        q = Task.getByUserId(g.user.id)
    status = -1
    if 'status' in request.args:
        q = q.filter(Task.status==request.args.get('status'))
        status = int(request.args.get('status'))
    if 'subject' in request.args:
        q = q.filter(Task.subject.like("%" + request.args.get('desc') + "%"))
    tasks = q.order_by(Task.create_time.desc()).all()
    if tasks and len(tasks) > 0:
        resp = []
        for m in tasks:
            res = {}
            res['id'] = m.id
            res['subject'] = m.subject
            res['teacher'] = u'无'
            res['create_time'] = str(m.create_time)
            res['content'] = m.desc
            if m.status == 1:
                res['status'] = u'已完成'
            else:
                res['status'] = u'未完成'
            u = User.getById(m.teacher_id)
            if u:
                res['teacher'] = u.name
            u = User.getById(m.student_id)
            if u:
                res['name'] = u.name
            resp.append(res)
        return render_template('task.html', user=g.user, tasks=resp, status=status);
    else:
        return render_template('task.html', user=g.user)

@bbs_app.route('/homework/add/', methods=['POST'])
@login_required
def addhomework():
    if g.user.priv != User.TEACHER:
        return render_template('error.html', user=g.user, error=u'haha')
    subject = request.form.get('subject', None)
    desc = request.form.get('content', None)
    group_id = request.form.get('group_id', None)
    resp = json_response()
    print group_id
    us = User.getByGroupId(group_id)
    print len(us)
    try:
        for u in us:
            mm = Task()
            mm.subject = subject
            mm.desc = desc
            mm.student_id = u.id
            mm.status = 0
            mm.teacher_id = g.user.id
            sess.add(mm)
        sess.commit()
        resp.data = json.dumps({'code':0, 'msg': u'发布成功'})
    except Exception, ex:
        resp.data = json.dumps({'code': -1, 'reason': ex})
    return resp

@bbs_app.route('/homework/do/<t_id>/', methods=['GET'])
@login_required
def dohomework(t_id):
    if g.user.priv != User.TEACHER:
        return render_template('error.html', user=g.user, error=u'haha')
    t = Task.getById(t_id)
    resp = json_response()
    try:
        t.status = 1
        sess.commit()
        resp.data = json.dumps({'code':0, 'msg': u'成功'})
    except Exception, ex:
        resp.data = json.dumps({'code': -1, 'reason': ex})
    return resp

