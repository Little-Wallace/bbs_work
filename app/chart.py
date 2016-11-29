from functools import wraps
import json
from flask import g, session, request, make_response, Response, url_for, flash
from flask.blueprints import Blueprint
from flask import render_template, redirect
from app import bbs_app
from models import User, Topic, Message, ChatInfo
from models import session as sess
from views import login_required
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, HiddenField, PasswordField
from wtforms.validators import Required
from datetime import datetime

# views_app = Blueprint('views_app', __name__)

class InputInfo(Form):
	content = TextAreaField('', validators=[Required()])
	submit = SubmitField('Send Enter')

class InputNameAndPassword(Form):
	username = StringField('', validators=[Required()])
	password = PasswordField('', validators=[Required()])
	submit = SubmitField('Login')

@bbs_app.route('/logout/', methods=['GET'])
@login_required
def logout():
	session['logged_in'] = False
	return redirect('/login/')

@bbs_app.route('/login/', methods=['GET', 'POST'])
def login():
	form = InputNameAndPassword()
	if form.validate_on_submit():
		id = form.username.data
		password = form.password.data
		user = User.check(id, password)
		if user:
			session['logged_in'] = True
			session['user_id'] = user.id
			g.user = user
			return redirect(url_for('index'))
		else:
			flash('Invalid username or password', 'danger')
	return render_template('login.html', form = form)

@bbs_app.route('/register/', methods=['GET', 'POST'])
def register():
	return render_template('register.html')

@bbs_app.route('/', methods=['GET'])
@login_required
def index():
	return render_template('base_csj.html', user = g.user)

@bbs_app.route('/chattinglist/', methods=['GET'])
@login_required
def chattinglist():
	users = User.getAll()
	return render_template('chattinglist.html', user = g.user, users = users)

@bbs_app.route('/communication/<other_id>', methods=['GET','POST'])
@login_required
def chat(other_id):
	a = ChatInfo.getBySenderAndTo(g.user.id, other_id)
	b = ChatInfo.getBySenderAndTo(other_id, g.user.id)
	mergelist = sorted(a+b, key = lambda ChatInfo:ChatInfo.create_time)
	form = InputInfo()
	if form.validate_on_submit():
		msg = form.content.data
		form.content.data = ''
		cc = ChatInfo(id=0, sender = g.user.id, to = other_id, content = msg)
		sess.add(cc)
		sess.commit()
		return redirect('/communication/' + other_id)
	return render_template('chat_room.html', information = mergelist, form = form, other_id = other_id)

@bbs_app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
	
@bbs_app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

