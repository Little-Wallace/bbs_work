from functools import wraps
import json
from flask import g, session, request, make_response, Response, url_for
from flask.blueprints import Blueprint
from flask import render_template, redirect
from app import bbs_app
from models import User, Topic, Message, ChatInfo
from models import session as sess
from views import login_required
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

# views_app = Blueprint('views_app', __name__)

class InputInfo(Form):
	content = TextAreaField('', validators=[Required()])
	submit = SubmitField('Send Enter')

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
