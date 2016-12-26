# 
sudo apt-get install python-setuptools
# 创建虚拟环境
sudo easy_install virtualenv
virtualenv venv
source venv/bin/activate
pip install Flask
# mysqldb相关依赖
sudo apt-get install libmysqlclient-dev
sudo apt-get install libxml2-dev libxslt1-dev python-dev
sudo apt-get install libevent-dev
sudo apt-get install zlib1g-dev

# pip freeze > requirements.txt # use this command to output the packages
pip install -r requirements.txt # install the packages # csj
 
