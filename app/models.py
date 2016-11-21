from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

__author__ = 'xixihaha'

Base = declarative_base()
engine = create_engine('mysql://root:123456@localhost:3306/bbs')
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

    create_time = Column(DateTime(), default=datetime.now())
    
    @classmethod
    def check(cls, name, passwd):
        return session.query(cls).filter(cls.name==name, cls.password==passwd).first()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

