from app.models import User

if __name__ == '__main__':
    u = User.check(name='jiangzemin', passwd='xxxx')
    if u:
        print u.name
    else:
        print 'None'

