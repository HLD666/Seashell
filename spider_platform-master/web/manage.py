"""
----------------------------------------数据库迁移创建使用-------------------------------------------------------------
提供以下几个命令:
python manage.py db init  用于初始化数据库，工程创建时候使用一次，回创建对应的Sql语句
python manage.py db migrate 用于工程中生产数据库变化，但还没有落库
python manage.py db upgrade 用于将数据库改变落库，此操作之后，数据库回发生改变。
一般model数据库修改之后，操作后两个命令，数据库就会更新
"""
import sys
sys.path.append("..")

from flask_script import Manager, Server
from app import app
from flask_migrate import Migrate, MigrateCommand
from exts import db
from common import models

manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand) # 创建数据库映射命令
manager.add_command('start', Server(port=8000, use_debugger=True)) # 创建启动命令

if __name__ == '__main__':
    manager.run()