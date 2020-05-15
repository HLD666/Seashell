import unittest

import redis
from node.app import create_app
from node.tests.redis_env import redis_pool, insert_test_list
from node.celery_task.task_read_redis import get_task_info_from_redis


class RedisTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        insert_test_list()

    def tearDown(self) -> None:
        self.app_context.pop()
        redis_conn = redis.Redis(connection_pool=redis_pool)
        redis_conn.flushdb()

    def test_pop_item(self):
        task_info = get_task_info_from_redis(redis_pool)

        self.assertEqual("1", task_info["id"])
        self.assertEqual("start", task_info["status"])

    def test_pop_task_when_current_running_is_max(self):
        pass

    @unittest.skip("not support")
    def test_put_back(self):
        pass
