#encoding: utf-8
from functools import wraps
import json
from flask import g, session, request, make_response, Response, url_for, flash
from flask.blueprints import Blueprint
from flask import render_template, redirect
from app import bbs_app
from models import User, Topic, Message, ChatInfo, Topic, NameList, Comment_Topic
from models import session as sess
from views import login_required
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, HiddenField, PasswordField
from wtforms.validators import Required, Email, Length
from datetime import datetime

# views_app = Blueprint('views_app', __name__)

class InputInfo(Form):
	content = TextAreaField('', validators=[Required()])
	submit = SubmitField('Send Enter')

class InputNameAndPassword(Form):
	username = StringField('', validators=[Email()])
	password = PasswordField('', validators=[Required()])
	submit = SubmitField('Login')

class InputOfTopic(Form):
	title = StringField('', validators=[Length(min=4, max=37)])
	content =TextAreaField('', validators=[Required()])
	submit = SubmitField('Launch Enter')

class InputOfRegister(Form):
	username = StringField('', validators=[Required()])
	email = StringField('', validators=[Email()])
	password = PasswordField('', validators=[Required()])
	submit = SubmitField('Register')

@bbs_app.route('/logout/', methods=['GET'])
@login_required
def logout():
	session['logged_in'] = False
	return redirect('/login/')

@bbs_app.route('/login/', methods=['GET', 'POST'])
def login():
    if session.has_key('logged_in') and session['logged_in'] and session['user_id']:
        print "xxxx"
        return redirect('/')
    print session['logged_in']
    print "....."
    form = InputNameAndPassword()
    if form.validate_on_submit():
        mail = form.username.data
        password = form.password.data
        user = User.check(mail, password)
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            g.user = user
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form = form)

@bbs_app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('base_csj.html', user = g.user)

@bbs_app.route('/chattinglist/', methods=['GET'])
@login_required
def chattinglist():
	users = User.getAll()
	return render_template('chattinglist.html', user = g.user, users = users, cur_page='chat')

@bbs_app.route('/communication/<int:other_id>', methods=['GET','POST'])
@login_required
def chat(other_id):
	a = ChatInfo.getBySenderAndTo(g.user.id, other_id)
	b = ChatInfo.getBySenderAndTo(other_id, g.user.id)
	mergelist = sorted(a+b, key = lambda ChatInfo:ChatInfo.create_time)
        for x in mergelist:
            print x.content
	form = InputInfo()
    	nname = User.getById(other_id).name
        if form.validate_on_submit():
		msg = form.content.data
                print msg
		form.content.data = ''
		cc = ChatInfo(id=0, sender=g.user.id, to=other_id, content=msg)
		sess.add(cc)
		sess.commit()
                print 'add succ'
		return redirect('/communication/' + str(other_id))
	return render_template('chat_room.html', information = mergelist, form = form, other_id =
                other_id, other_name = nname)

@bbs_app.route('/communication/<int:other_id>/get/', methods=['GET'])
@login_required
def get_chat_info(other_id):
    a = ChatInfo.getBySenderAndTo(g.user.id, other_id)
    b = ChatInfo.getBySenderAndTo(other_id, g.user.id)
    mergelist = sorted(a+b, key = lambda ChatInfo:ChatInfo.create_time)
    nname = User.getById(other_id).name
    for x in mergelist:
        print 'xxx=', x.content
    	nname = User.getById(other_id).name
    return render_template('chat_info.html', information = mergelist, other_id = other_id, other_name=nname)

@bbs_app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
	
@bbs_app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@bbs_app.route('/bbslist/<int:id>', methods=['GET'])
@login_required
def bbs_list(id):
	if id == 0:
		topic = Topic.getAll()
	else:
		topic = Topic.getByFlag(id-1)
	return render_template('bulletin_board_list.html', user = g.user, topic = topic, NameList =
                NameList, User = User, cur_page='bbs', comment_topic = Comment_Topic)

@bbs_app.route('/addtopic/<int:t_id>', methods=['GET', 'POST'])
@login_required
def addtopic(t_id):
	form = InputOfTopic()
	if t_id != 0:
		topic = Topic.getById(t_id)
		form.content.data = topic.content
		form.title.data = topic.title
	if form.validate_on_submit():
		flag_id = request.form['radioInline']
		title = form.title.data
		content = form.content.data
		if t_id != 0:
			sess.query(Topic).filter(Topic.id == t_id).update({Topic.content : content, Topic.author : g.user.id, Topic.title : title, Topic.flag : flag_id})
		else:
			sess.add(Topic(id = 0, content = content, author = g.user.id, title = title, flag = flag_id))
		sess.commit()
		return redirect('/bbslist/0')
	return render_template('add_topic.html', user = g.user, form = form)

@bbs_app.route('/register/', methods=['GET', 'POST'])
def register():
	form = InputOfRegister()
	if form.validate_on_submit():
		name = form.username.data
		pswd = form.password.data
		email = form.email.data
		form.username.data = ""
		form.password.data = ""
		form.email.data = ""
		if User.checkByEmail(email):
			flash('This email has been used!', 'danger')
		else:
			sess.add(User(id=0, name = name, password = pswd , email= email))
			sess.commit()
			g.user = User.checkByEmail(email)
			session['logged_in'] = True
			session['user_id'] = g.user.id
			return redirect('/')
	return render_template('register.html', form = form)		

@bbs_app.route('/topic/<int:id>', methods=['GET', 'POST'])
@login_required
def topic(id):
	topic = Topic.getById(id)
	content = topic.content.split('\n')
	comment = sorted(Comment_Topic.getByTopic(id), key = lambda Comment_Topic:Comment_Topic.create_time)
	form = InputInfo()
	if form.validate_on_submit():
		msg = form.content.data
		form.content.data = ""
		sess.add(Comment_Topic(id = 0, content = msg, author = g.user.id, topic_id = id))
		sess.commit()
		return redirect('/topic/' + str(id))
        resp = []
        for c in comment:
            res = {}
            res['topic_id'] = c.topic_id
            res['content'] = c.content
            res['author'] = c.author
            res['head'] = User.getById(c.author).head
            res['create_time'] = c.create_time
            resp.append(res)
	return render_template('topic_content.html', user = g.user, t = topic, User = User, NameList = NameList, content = content, comment = resp, form = form)
