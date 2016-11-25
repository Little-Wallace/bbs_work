from app.models import User, session, Group
from flask import url_for

if __name__ == '__main__':
    u = session.query(User).first()
    g = session.query(Group).all()
    print u.group_id
    for r in g:
        print r.id

