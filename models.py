from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'xixihaha'

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))

engine = create_engine('mysql://root:123456@localhost:3306/bbs')
DBsession = sessionmaker(bind=engine)

if __name__ == '__main__':
    session = DBsession()
    Base.metadata.create_all(engine)
