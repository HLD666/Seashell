from node.app import scheduler
from node.db.exts import redis_pool

from common.log import log

from spider.task_list import task_list
from node.core.get_task import *
from node.core.load_task import *
from node.core.global_parameter import current_task_list, node_running_info


def start_read():
    with scheduler.app.app_context():
        log.debug("Start to read redis to get task.")
        print("start to read redis.")

        if len(current_task_list) >= node_running_info.get("max_ps", 5):
            log.debug("There is too many task now, wait to get new..")
        else:
            log.debug(f"Start to read redis in {redis_pool.connection_kwargs}")
            task_info_redis = get_task_info_from_redis(redis_pool)
            print(f"get task: {task_info_redis}")
            log.debug(f"get task: {task_info_redis}")

            if task_info_redis is not None and task_info_redis["status"] == "start":
                task_info = get_task_info_with_id(task_info_redis["id"])
                task_location_info = get_the_task_info_from_register_list(task_info["template"], task_list)
                task_info.update(task_location_info)
                print(task_info)

                start_the_task_with_task_info(task_info)
