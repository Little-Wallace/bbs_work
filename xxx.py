#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment
from flask import url_for
from app import bbs_app
from datetime import datetime
import json
import re

if __name__ == '__main__':
    a = session.query(Article).first()
    re_h = re.compile('</?\w+[^>]*>')
    s = re_h.sub('', a.content)
    print a.content
    print s

