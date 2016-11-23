from app import bbs_app

if __name__ == '__main__':
    print bbs_app.url_map
    bbs_app.run(host='0.0.0.0', port=8888)

