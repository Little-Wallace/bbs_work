#encoding: utf-8
from app.models import User, session, Message
from flask import url_for
from app import bbs_app

if __name__ == '__main__':
    print bbs_app.config

