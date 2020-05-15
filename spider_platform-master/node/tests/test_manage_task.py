import unittest
import time
import importlib
from multiprocessing import Process

from node.app import create_app
from node.db.exts import db

from node.core.load_task import *
from node.tests.spider.task_list import task_list
from node.core.global_parameter import current_task_list


class TaskManageTestCase(unittest.TestCase):
    test_task_id = 1
    test_table_name = "res_1_test0001"
    test_spider_path = "node.tests.spider.crawl.weather_get_city_list"
    test_spider_class = "CityList"

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()

    @staticmethod
    def pretend_spider_task(sleep_time):
        time.sleep(sleep_time)

    def test_stop_the_running_task(self):
        # task = Process(target=lambda x: time.sleep(x), args=(5,))
        task = Process(target=self.pretend_spider_task, args=(5,))
        task.start()
        task_name = task.name
        task_id = 1

        # put_task_into_flask_g(task, task_id)

        self.assertEqual(task_name, current_task_list[1].name)
        task.join()
