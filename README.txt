# 
sudo apt-get install python-setuptools
# 创建虚拟环境
sudo easy_install virtualenv
virtualenv venv
source venv/bin/activate
pip install Flask
pip install SQLAlchemy
# mysqldb相关依赖
sudo apt-get install libmysqlclient-dev
sudo apt-get install libxml2-dev libxslt1-dev python-dev
sudo apt-get install libevent-dev
sudo apt-get install zlib1g-dev
pip install MySQL-python


