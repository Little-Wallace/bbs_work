#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment
from flask import url_for
from app import bbs_app
from datetime import datetime
import json
import re

if __name__ == '__main__':
    u = User.getById(1)
    u.priv = 'teacher'
    uu = User.getById(2)
    uu.group_id = 3
    base_score = 80
    al = session.query(Article).all()
    for a in al:
        print a.id
        content = a.content
        t = ArticleToUser() 
        t.article_id = a.id
        t.user_id = 1
        session.add(t)
    ''' 
    print content
    for i in range(0, 10): 
        g = Grade()
        g.semester = u'春季学期'
        g.teacher_id = 1
        g.student_id = 3
        g.score = 90 + i * nu;
        g.subject = u"数学"
        g.name = User.getById(3).name
        nu *= -1
        session.add(g)
    '''
    session.commit()
    


