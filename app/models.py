# encoding: utf-8
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TEXT
from datetime import datetime

__author__ = 'xixihaha'

Base = declarative_base()
engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/bbs?charset=utf8', echo=True)
DBsession = sessionmaker(bind=engine)
session = DBsession()

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
    sign_time = Column(DateTime(), default=datetime.now())
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
    desc = Column(TEXT)
    author = Column(String(28))
    style = Column(Integer())
    title = Column(String(36))
    create_time = Column(DateTime(), default=datetime.now())


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
    u = User(id=198964, group_id=123)
    u.name=u'江泽民'
    u.password='xixihaha'
    l = Message(id=123)
    l.desc = u'敢同恶鬼争高下' 
    l.title = u'一派胡言'
    l.status = u'未读'
    g = Group(id=123)
    g.name= u'三年级二班'
    g.teacher=u'北大教授王铁崖'
    session.add(u)
    session.add(l)
    session.add(g)
    session.commit()
