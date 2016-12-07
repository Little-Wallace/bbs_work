#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment
from flask import url_for
from app import bbs_app
from datetime import datetime
import json
import re

if __name__ == '__main__':
    u = session.query(User).first()
    u.head = 'img/saber.png'
    session.commit()

