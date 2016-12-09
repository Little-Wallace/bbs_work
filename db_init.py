#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment, ChatInfo, Topic, Comment_Topic
from flask import url_for
from app import bbs_app
from datetime import datetime
import json
import re

if __name__ == '__main__':
    session.commit()
    a = User(id=0, name = "Sijia", password = "11", email='sijia@gmail.com', head = "img/s1.jpg",
            phone = "13141314776", group_id = 1)
    b = User(id=0, name = "Liuwei", password = "11", email='liuwei@gmail.com', head = "img/s2.jpg",
            phone = "13111111444", group_id = 3)
    c = User(id=0, name = "Baihao", password = "11", email='baihao@gmail.com', head = "img/s3.jpg",
            phone = "19872635168", group_id = 3)
    d = User(id=0, name = "Jingsheng", password = "11", email='jinsheng@gmail.com', head =
            "img/s4.jpg", phone = "13413423287", group_id = 2)
    e = User(id=0, name = "Lianzhuang", password = "11", email='lianzhuang@gmail.com', head =
            "img/s5.jpg", phone = "17263927635", group_id = 2)
    f = User(id=0, name = "Peilin", password = "11", email='peilin@gmail.com', head = "img/s6.jpg",
            phone = "13413423134", group_id = 4)
    session.add(a)
    session.add(b)
    session.add(c)
    session.add(d)
    session.add(e)
    session.add(f)

    ca = ChatInfo(id=0, sender = 1, to = 2, content = 'Do you have the breakfast?')
    cb = ChatInfo(id=0, sender = 2, to = 1, content = 'No, I have the lunch.')
    cc = ChatInfo(id=0, sender = 1, to = 2, content = 'Wow, you must eat rice and meat.')
    dd = ChatInfo(id=0, sender = 2, to = 1, content = 'Yeah, you are right!')
    session.add(ca)
    session.add(cb)
    session.add(cc)
    session.add(dd)
    
    session.add(Topic(id = 0, content = ''' Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web.\n One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.\n "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully between its four familiar walls. \nA collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who s\n''', title = "My First Topic in MoMo BBS", flag = 1, author = 1))
    session.add(Topic(id = 0, content =
        u"以前和计算机院的学姐住的时候，厕所还好好的，如今学姐走了，来了国院的妹子，好家伙，真是长见识！上厕所有人解锁新姿势，屁股朝外，大号还不锁门，干啥玩意儿，直播拉翔等着给你送兰博基尼啊！一个个的小便大便都不带冲厕所的，怎么地，攒肥卖钱啊，金坷垃奏是你们代言的，倒是把自己收拾的挺干净，知不知道你上完的厕所也是你的另一张脸，这么大人了这点事还要我提醒，真是心累", title = u"金坷垃,亩产一万八", flag = 2, author = 2))
    session.add(Topic(id = 0, content = 
        u'失眠了\n还有15天。时间过的好快好快，越复习越觉得时间不够，最近做真题都有点患得患失了，怕自己考不上\n有时看书看得眼睛花脑仁疼也得坚持学到十点多再回宿舍，因为自习室里大家都还在奋斗。上次老妈还说给我算了个命，老先生说我能考上。每天也都会告诉自己不要担心，心态要放平和点。\n嗯，还是不要想那么多了，脚踏实地走好每一步，所有的努力都不会白费~ \n愿大家都能取得满意的结果，共勉~', title = u"但行好事，莫问前程", flag = 3, author = 3))
    session.add(Comment_Topic(id = 0, content = "This is a very useful topic", author = 1, topic_id = 1))	
    session.add(Comment_Topic(id = 0, content = "I like it very much!!!", author = 2, topic_id = 1))
    session.add(Comment_Topic(id = 0, content = "Thanks for sharing", author = 3, topic_id = 1))
    session.add(Comment_Topic(id = 0, content =
        u"非国院飘过…画面太美233，不过毕竟这应该是个人行为，不能代表国院的同学吧。楼里就别开地图炮了就事论事就好。 \n拉粑粑不冲的行为真是巨恶心…是不是觉得自己的那啥特别有造型想让别人看...", author = 4, topic_id = 2))	
    session.add(Comment_Topic(id = 0, content = u"这位国院的妹子只代表她自己不代表国院!!!", author =
        5, topic_id = 2))
    session.add(Comment_Topic(id = 0, content = "Thanks for sharing", author = 6, topic_id = 3))
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
    u = session.query(User).first()
    print u.priv
    u.priv = 'admin'
    session.commit()

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

