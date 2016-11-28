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
	form.username.data = 198964
	form.password.data = 'xixihaha'
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

@bbs_app.route('/communication/', methods=['GET','POST'])
@login_required
def chat():
	Information = ChatInfo.getAll()
	form = InputInfo()
	if form.validate_on_submit():
		msg = form.content.data
		form.content.data = ''
		cc = ChatInfo(id=0, sender = g.user.name, to = 'xixi', content = msg)
		sess.add(cc)
		sess.commit()
		return redirect(url_for('chat'))
	return render_template('chat_room.html', information = Information, form = form)
