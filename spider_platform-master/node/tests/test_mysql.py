import unittest
import datetime

from common.models import SpiderTask, SpiderTemplate, Category, Website

from node.app import create_app
from node.db.exts import db
from node.core.get_task import get_task_info_with_id


class MysqlTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.insert_test_task_in_spider_task_table()

    def tearDown(self) -> None:
        # db.drop_all()
        db.session.remove()
        self.app_context.pop()

    @classmethod
    def insert_test_task_in_spider_task_table(cls):
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

    def test_get_task_info(self):
        task_info = get_task_info_with_id("1")

        self.assertEqual(1, task_info["id"])
        self.assertEqual("测试任务01", task_info["name"])
        self.assertEqual(1, task_info["template"])
        self.assertEqual(4, task_info["status"])
        self.assertEqual("res_1_0000000001", task_info["table"])
