import datetime
from flask import Flask
from node.config.app_config import config
from common.models import SpiderTask, SpiderTemplate, Category, Website
from common.models import db

from sqlalchemy import create_engine
from spider.standard.spider_demo import Base


def create_app(start_type):
    app = Flask(__name__)
    app.config.from_object(config[start_type])
    config[start_type].init_app(app)
    print(app.config.get("SQLALCHEMY_DATABASE_URI"))
    db.init_app(app)

    return app


def insert_test_task_in_spider_task_table():
    category = Category(name="测试")
    db.session.add(category)
    db.session.commit()

    website = Website(name="测试网站", description="测试用", is_hot="1", category_id=1)
    db.session.add(website)
    db.session.commit()

    template = SpiderTemplate(name="测试任务", website_id=1, category_id=1, para_file="test.csv")
    db.session.add(template)
    db.session.commit()

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task = SpiderTask(name="测试任务01", template_id=1, is_timing=0, status=4,
                      execute_cycle=0, publish_time=time_now, paras_table="res_1_0000000001")
    db.session.add(task)
    db.session.commit()


def insert_test_task_in_spider_task_table2():
    category = Category(name="京东")
    db.session.add(category)
    db.session.commit()

    website = Website(name="京东搜索", description="抓取京东搜索内容", is_hot="1", category_id=1)
    db.session.add(website)
    db.session.commit()

    template = SpiderTemplate(name="京东搜索", website_id=2, category_id=2, para_file="test2.csv")
    db.session.add(template)
    db.session.commit()

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task = SpiderTask(name="京东搜索任务", template_id=1, is_timing=0, status=4,
                      execute_cycle=0, publish_time=time_now,
                      paras_table="jd_demo", res_table="res_2_0000000001")
    db.session.add(task)
    db.session.commit()


db_information = {"host": "127.0.0.1",
                  "user": "admin",
                  "password": "1q2w3e4r",
                  "database": "res_data",
                  "charset": "utf8",
                  "port": "3306"}


def create_the_pretend_result_table():
    engine = create_engine(f'mysql+pymysql://{db_information["user"]}:{db_information["password"]}'
                           f'@{db_information["host"]}:{db_information["port"]}'
                           f'/{db_information["database"]}?charset={db_information["charset"]}',
                           pool_recycle=3600)

    Base.metadata.create_all(engine)


def single_insert_a_spider_task():
    flask_app = create_app('development')
    flask_context = flask_app.app_context()
    flask_context.push()

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task = SpiderTask(name="京东热门列表（selenium）", template_id=3, is_timing=0, status=4,
                      execute_cycle=0,  task_type=0, publish_time=time_now, node_type=0,
                      paras_table="tb_jd_hotlist_task", res_table="tb_jd_hotlist_data")
    db.session.add(task)
    db.session.commit()

    flask_context.pop()


if __name__ == "__main__":
    # create_the_pretend_result_table()
    # insert_test_task_in_spider_task_table2()
    single_insert_a_spider_task()
