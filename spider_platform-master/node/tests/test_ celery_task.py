import unittest
import importlib
from multiprocessing import Process

import pytest

from node.app import create_app
from node.db.exts import db
from node.celery_task import make_celery

from node.celery_task.task_start_and_maintain import implement_task


class TaskLoadTestCase(unittest.TestCase):
    test_task_id = 1
    test_table_name = "res_1_test0001"
    test_spider_path = "node.tests.spider.crawl.weather_get_city_list"
    test_spider_class = "CityList"

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.celery_app = make_celery(self.app)
        self.celery_app.conf.update(CELERY_ALWAYS_EAGER=True)

        celery_start_argv = ['worker', '-B', '-s', 'celery_schedule_bak/celery_schedule']
        self.celery_process = Process(target=self.celery_app.worker_main, args=(celery_start_argv,))
        self.celery_process.start()
        self.create_the_result_table()

    def tearDown(self) -> None:
        self.app_context.pop()
        self.celery_process.close()

    def create_the_result_table(self):
        database_url = self.app.config.get("SQLALCHEMY_DATABASE_URI")
        print(database_url)

        module = importlib.import_module(self.test_spider_path, package=__package__)
        module.create_result_table(self.test_table_name, database_url)
        self.db_class = module.result_table_creator(self.test_table_name)

    def test_implement_task_with_celery(self):
        code = implement_task.delay().get()
        self.assertEqual(0, code)
