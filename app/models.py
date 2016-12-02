# encoding: utf-8
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, Integer, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.sql import func
from datetime import datetime

__author__ = 'xixihaha'

Base = declarative_base()
engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/bbs?charset=utf8')
DBsession = sessionmaker(bind=engine)
session = DBsession()
NameList = [('Math','default') ,('English','primary'), ('Chemistry','success'), ('Sport','info'), ('Psychology','warning'), ('Computer Science', 'danger')]

class User(Base):

    STUDENT = 'stu'
    PARENT = 'par'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    ROOT = 'root'

    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    password = Column(String(32))
    phone = Column(String(20))
    priv = Column(String(16), default=STUDENT)
    sex = Column(String(20))
    major = Column(String(30))
    university = Column(String(32))
    status = Column(String(20))
    school = Column(String(20))
    qq = Column(String(20))
    email = Column(String(64))
    extra = Column(String(256))
    id_card = Column(String(32))
    group_id=Column(Integer())
    address = Column(String(32))


    create_time = Column(DateTime(), default=datetime.now())

 
    @classmethod
    def check(cls, mail, passwd):
        return session.query(cls).filter(cls.email==mail, cls.password==passwd).first()

    @classmethod
    def getById(cls, id):
        return session.query(cls).filter(cls.id==id).first()

    @classmethod
    def getByGroupId(cls, id):
        return session.query(cls).filter(cls.group_id==id).all()

    @classmethod
    def getAll(cls):
        return session.query(cls).all()

class ChatInfo(Base):
	
    __tablename__ = 'chatinfo'

    id = Column(Integer(), primary_key = True)
    sender = Column(String(256))
    to = Column(String(256))
    content = Column(String(256))
    create_time = Column(DateTime(timezone=True), default=func.now())
	
    @classmethod
    def getAll(cls):
        return session.query(cls).all()
    @classmethod
    def getBySenderAndTo(cls, sender_id, to_id):
        return session.query(cls).filter(cls.sender == sender_id and cls.to == to_id).all()

class Message(Base):

    __tablename__ = 'message'

    id = Column(Integer(), primary_key=True)
    desc = Column(TEXT)
    title = Column(String(256))
    style = Column(String(32))
    status = Column(Integer())
    author_id = Column(String(20))
    user_id = Column(Integer())
    group_id = Column(Integer())
    create_time = Column(DateTime(), default=func.now())

    @classmethod
    def getById(cls, id):
        return session.query(cls).filter(cls.id==id).first()

    @classmethod
    def getByGroupId(cls, group_id, user_id):
        return session.query(cls).filter(or_(cls.group_id==group_id, cls.author_id==user_id,
            cls.user_id==user_id))

class Grade(Base):

    __tablename__ = 'grade'

    id = Column(Integer(), primary_key=True)
    semester = Column(String(28))
    contest_time = Column(DateTime(), default=func.now())
    teacher_id = Column(Integer())
    student_id = Column(Integer())
    score = Column(Integer())
    subject = Column(String(32))
    name = Column(String(32))

    @classmethod
    def getById(cls, id):
        return session.query(cls).filter(cls.id==id).first()

    @classmethod
    def getByUserId(cls, id):
        return session.query(cls).filter(cls.student_id==id)

    @classmethod
    def getByTeacherId(cls, id):
        return session.query(cls).filter(cls.teacher_id==id)

class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer(), primary_key=True)
    create_time = Column(DateTime(), default=func.now())
    teacher_id = Column(Integer())
    student_id = Column(Integer())
    status = Column(Integer())
    subject = Column(String(32))
    desc = Column(TEXT)

    @classmethod
    def getByUserId(cls, id):
        return session.query(cls).filter(cls.student_id==id).order_by(cls.create_time.desc())

    @classmethod
    def getByTeacherId(cls, id):
        return session.query(cls).filter(cls.teacher_id==id).order_by(cls.subject)

    @classmethod
    def getById(cls, id):
        return session.query(cls).filter(cls.id==id).first()



class Topic(Base):

    __tablename__ = 'topic'

    id = Column(Integer(), primary_key=True)
    content = Column(TEXT)
    author = Column(Integer())
    flag = Column(Integer())
    title = Column(String(36))
    create_time = Column(DateTime(timezone=True), default=func.now())	
    @classmethod
    def getAll(cls):
        return session.query(cls).all()
    @classmethod
    def getByid(cls, id):
        return session.query(cls).filter(cls.id==id).first()
    @classmethod
    def getByFlag(cls, flag_id):
        return session.query(cls).filter(cls.flag==flag_id).all()
    @classmethod
    def getByAuthor(cls, author_id):
        return session.query(cls).filter(cls.author==author_id).all()

class Comment_Topic(Base):
    
    __tablename__ = 'comment_topic'
    
    id = Column(Integer(), primary_key=True)
    content = Column(TEXT)
    author = Column(Integer())
    topic_id = Column(Integer())
    create_time = Column(DateTime(timezone=True), default=func.now())

    @classmethod
    def getAll(cls):
        return session.query(cls).all()
    @classmethod
    def getByTopic(cls, topic_id):
	return session.query(cls).filter(cls.topic_id == topic_id).all()

class Article(Base):

    __tablename__ = 'article'

    id = Column(Integer(), primary_key=True)
    title = Column(String(36))
    content = Column(TEXT)
    author = Column(String(28))
    style = Column(Integer())
    dest = Column(Integer())
    create_time = Column(DateTime(), default=func.now())
    picture_dir = Column(String())

class Comment(Base):

    __tablename__ = 'comment'

    id = Column(Integer(), primary_key=True)
    desc = Column(TEXT)
    author = Column(String(28))
    dest = Column(Integer())
    topic_id = Column(Integer())

    create_time = Column(DateTime(), default=datetime.now())


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
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
    session.add(Topic(id = 0, content = "WoLeigequ", title = "My First Topic in MoMo BBS", flag = 1, author = 1))
    session.add(Topic(id = 0, content = "LiuweiLiuxiaowei", title = "Liuwei's new girl-friend", flag = 2, author = 2))
    session.add(Topic(id = 0, content = "XiXi XiXi HaHa", title = "Do you know I mean what??", flag = 3, author = 3))
    session.add(Topic(id = 0, content = "sdadasda", title = "Do you love me?", flag = 4, author = 4))
    session.commit()
