#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment, Task
from flask import url_for
from app import bbs_app
from datetime import datetime
import json
import re

if __name__ == '__main__':
    for g in session.query(Grade).all():
        print g.student_id
        print g.score
    session.commit()
    for i in range(0, 10):
        t = Task()
        t.name = 'haha'
        t.teacher_id = 1
        t.student_id = i + 1
        t.status = 0
        t.subject = u'人生的经验'
        t.desc = u'与长者谈笑风生'
    #    session.add(t)
    session.commit()

