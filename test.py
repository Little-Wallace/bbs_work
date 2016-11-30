#encoding: utf-8
from app.models import User, session, Message
from flask import url_for

if __name__ == '__main__':
    u = User.getById(1)
    u.priv = 'teacher'
    session.commit()

