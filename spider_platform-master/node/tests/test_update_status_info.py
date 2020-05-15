import unittest
import datetime

from common.models import SpiderTask, SpiderTemplate, Category, Website
from node.app import create_app
from node.db.exts import db

from node.core.update_info import *
from node.core.get_self_info import generate_node_info


class StatusUpdateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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

    def test_upload_node_info(self):
        upload_this_node_info()
        node_info = generate_node_info()

        node_info_db = db.session.query(Node).filter(Node.id == 1).first()

        self.assertEqual(node_info["ip_addr"], node_info_db.ip_addr)
        self.assertEqual(node_info["host_name"], node_info_db.host_name)
        self.assertEqual(node_info["node_type"], node_info_db.node_type)
        self.assertEqual(node_info["max_ps"], node_info_db.max_ps)
        self.assertEqual(node_info["cur_ps"], node_info_db.cur_ps)
        self.assertEqual(node_info["status"], node_info_db.status)

    def test_update_task_status(self):
        self.insert_test_task_in_spider_task_table()
        update_the_task_status(1, 2)

        task_info = db.session.query(SpiderTask).filter(SpiderTask.id == 1).first()

        self.assertEqual(2, task_info.status)
