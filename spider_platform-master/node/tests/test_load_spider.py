import unittest
import time
import importlib
from multiprocessing import Process

from node.app import create_app
from node.db.exts import db

from node.core.load_task import *
from node.tests.spider.task_list import task_list
from node.core.global_parameter import current_task_list


class TaskLoadTestCase(unittest.TestCase):
    test_task_id = 1
    test_table_name = "res_1_test0001"
    test_spider_path = "node.tests.spider.crawl.weather_get_city_list"
    test_spider_class = "CityList"

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.create_the_result_table()

    def tearDown(self) -> None:
        self.app_context.pop()

    def create_the_result_table(self):
        database_url = self.app.config.get("SQLALCHEMY_DATABASE_URI")
        print(database_url)

        module = importlib.import_module(self.test_spider_path, package=__package__)
        module.create_result_table(self.test_table_name, database_url)
        self.db_class = module.result_table_creator(self.test_table_name)

    def test_get_the_task_info(self):
        task_location_info = get_the_task_info_from_register_list(1, task_list)

        self.assertEqual("node.tests.spider.crawl.weather_get_city_list", task_location_info["file_path"])
        self.assertEqual("CityList", task_location_info["class_name"])

    def test_load_the_task_code(self):
        task_info = {"id": 1, "name": "测试任务01", "template": 1, "status": 4,
                     "table": self.test_table_name,
                     "file_path": self.test_spider_path,
                     "class_name": self.test_spider_class}

        start_the_task_with_task_info(task_info)

        module = importlib.import_module(self.test_spider_path, package=__package__)
        db_class = module.result_table_creator(self.test_table_name)
        city_info = db.session.query(db_class).filter(db_class.id == 1).first()

        self.assertEqual("北京", city_info.city_name)
        self.assertEqual("101010100", city_info.city_code)
        self.assertTrue(city_info.flag)
        self.assertTrue(city_info.queried)

    @staticmethod
    def pretend_spider_task(sleep_time):
        time.sleep(sleep_time)

    def test_save_the_spider_info(self):
        # task = Process(target=lambda x: time.sleep(x), args=(5,))
        task = Process(target=self.pretend_spider_task, args=(5,))
        task.start()
        task_name = task.name
        task_id = 1

        # put_task_into_flask_g(task, task_id)

        self.assertEqual(task_name, current_task_list[1].name)
        task.join()

    @unittest.skip("Noting to test.")
    def test_get_register_info(self):
        pass


