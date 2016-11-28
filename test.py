#encoding: utf-8
from app.models import User, session, Group, ChatInfo
from flask import url_for

if __name__ == '__main__':
    c = ChatInfo()
    c.content = u'蛤蛤'
    session.add(c)
    session.commit()

