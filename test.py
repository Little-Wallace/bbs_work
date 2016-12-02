#encoding: utf-8
from app.models import User, session, Message, Grade
from flask import url_for
from app import bbs_app
from datetime import datetime

if __name__ == '__main__':
    u = User.getById(1)
    u.priv = 'teacher'
    uu = User.getById(2)
    u.group_id = 3
    base_score = 80
    res = session.query(Grade).all()
    for t in res:
        t.name = u'习习蛤蛤'
        t.teacher_id = 1
    session.commit()

    


