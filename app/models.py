# encoding: utf-8
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.sql import func

__author__ = 'xixihaha'

Base = declarative_base()
engine = create_engine('mysql+mysqldb://root:l1admin@localhost:3306/bbs?charset=utf8', echo=True)
DBsession = sessionmaker(bind=engine)
session = DBsession()
NameList = [('Math','default') ,('English','primary'), ('Chemistry','success'), ('Sport','info'), ('Psychology','warning'), ('Computer Science', 'danger')]

class User(Base):

    STUDENT = 0
    PARENT = 1
    TEACHER = 2
    ADMIN = 3
    ROOT = 4

    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    password = Column(String(32))
    phone = Column(String(20))
    identity = Column(Integer(), default=STUDENT)
    sex = Column(String(20))
    major = Column(String(30))
    target_major = Column(String(30))
    university = Column(String(32))
    status = Column(String(20))
    school = Column(String(20))
    qq = Column(String(20))
    email = Column(String(20))
    sign_time = Column(DateTime(timezone=True), default=func.now())
    extra = Column(String(256))
    id_card = Column(String(32))
    test_number = Column(String(32))
    group_id=Column(Integer())
    register_level = Column(String(32))
    address = Column(String(32))


    create_time = Column(DateTime(), default=datetime.now())

 
    @classmethod
    def check(cls, name, passwd):
        return session.query(cls).filter(cls.id==name, cls.password==passwd).first()

    @classmethod
    def getById(cls, id):
        return session.query(cls).filter(cls.id==id).first()

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
    desc = Column(String(256))
    title = Column(String(256))
    style = Column(String(32))
    status = Column(String(20))
    author = Column(String(20))
    user_id = Column(Integer())
    create_time = Column(DateTime(), default=datetime.now())

    @classmethod
    def getById(cls, id):
        return session.query(cls).filter(cls.id==id).first()

    @classmethod
    def getByUserId(cls, id):
        return session.query(cls).filter(cls.user_id==id).first()

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
    desc = Column(TEXT)
    author = Column(String(28))
    style = Column(Integer())
    dest = Column(Integer())
    create_time = Column(DateTime(), default=datetime.now())

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
	a = User(id=0, name = "ChenSijia", password = "11")
	b = User(id=0, name = "Liuwei", password = "11")
	c = User(id=0, name = "Baihao", password = "11")
	d = User(id=0, name = "Wujingsheng", password = "11")
	session.add(a)
	session.add(b)
	session.add(c)
	session.add(d)
	ca = ChatInfo(id=0, sender = 1, to = 2, content = 'aa')
	cb = ChatInfo(id=0, sender = 2, to = 1, content = 'bb')
	cc = ChatInfo(id=0, sender = 1, to = 2, content = 'cc')
	dd = ChatInfo(id=0, sender = 2, to = 1, content = 'dd')
	session.add(ca)
	session.add(cb)
	session.add(cc)
	session.add(dd)
	session.add(Topic(id = 0, content = "WoLeigequ", title = "My First Topic in MoMo BBS", flag = 1, author = 1))
	session.add(Topic(id = 0, content = "LiuweiLiuxiaowei", title = "Liuwei's new girl-friend", flag = 2, author = 2))
	session.add(Topic(id = 0, content = "XiXi XiXi HaHa", title = "Do you know I mean what??", flag = 3, author = 3))
	session.add(Topic(id = 0, content = "sdadasda", title = "Do you love me?", flag = 4, author = 4))
	session.commit()
