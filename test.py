from app.models import User, session

if __name__ == '__main__':
    u = User(id=198964)
    u.name='jiangzemin'
    u.password='xixihaha'
    session.add(u)
    session.commit()
    if u:
        print u.name
    else:
        print 'None'

