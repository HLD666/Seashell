from node.db.exts import redis_pool
from node.start_app import celery_app

from spider.task_list import task_list
from node.core.get_task import *
from node.core.load_task import *


@celery_app.task()
def start_task():
    task_info_redis = get_task_info_from_redis(redis_pool)

    if task_info_redis is not None and task_info_redis["status"] == "start":
        task_info = get_task_info_with_id(task_info_redis["id"])
        task_location_info = get_the_task_info_from_register_list(task_info["id"], task_list)
        task_info.update(task_location_info)

        start_the_task_with_task_info(task_info)
