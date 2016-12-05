#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment
from flask import url_for
from app import bbs_app
from datetime import datetime
import json
import re

if __name__ == '__main__':
    session.commit()
    a = User(id=0, name = "ChenSijia", password = "11", email='xixihaha@gmail.com')
    b = User(id=0, name = "Liuwei", password = "11", email='xixihaha@gmail.com')
    c = User(id=0, name = "Baihao", password = "11", email='hhhh@gmail.com')
    d = User(id=0, name = "Wujingsheng", password = "11", email='xxxx@gmail.com')
    l = Message(id=123)
    l.desc = 'XIXI' 
    l.title = 'XIXI'
    l.status = 0
    ca = ChatInfo(id=0, sender = 1, to = 2, content = 'aa')
    cb = ChatInfo(id=0, sender = 2, to = 1, content = 'bb')
    cc = ChatInfo(id=0, sender = 1, to = 2, content = 'cc')
    dd = ChatInfo(id=0, sender = 2, to = 1, content = 'dd')
    session.add(ca)
    session.add(cb)
    session.add(cc)
    session.add(dd)
    #g = Group(id=123)
    # g.name= u'三年级二班'
    # g.teacher=u'北大教授王铁崖'
    session.add(a)
    session.add(b)
    session.add(c)
    session.add(d)
    session.add(l)
    session.add(Topic(id = 0, content = ''' Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web.\n One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.\n "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully between its four familiar walls. \nA collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who s\n''', title = "My First Topic in MoMo BBS", flag = 1, author = 1))
    session.add(Topic(id = 0, content = "LiuweiLiuxiaowei", title = "Liuwei's new girl-friend", flag = 2, author = 2))
    session.add(Topic(id = 0, content = "XiXi XiXi HaHa", title = "Do you know I mean what??", flag = 3, author = 3))
    session.add(Topic(id = 0, content = "sdadasda", title = "Do you love me?", flag = 4, author = 4))
    session.add(Comment_Topic(id = 0, content = "This is a very useful topic", author = 1, topic_id = 1))	
    session.add(Comment_Topic(id = 0, content = "This is a very useful topic", author = 2, topic_id = 1))
    session.add(Comment_Topic(id = 0, content = "This is a very useful topic", author = 3, topic_id = 1))
    session.commit()   
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


