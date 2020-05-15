import re
import redis

from common import common_config
from common.models import SpiderTask
from common import log

from node.app import PLATFORM
from node.db.exts import db


def get_task_info_with_id(task_id):
    task_info = db.session.query(SpiderTask).filter(SpiderTask.id == task_id).first()

    return {"id": int(task_id), "name": task_info.name, "template": task_info.template_id,
            "status": task_info.status, "paras_table": task_info.paras_table, "res_table": task_info.res_table}


def get_task_info_from_redis(use_redis_pool):
    if PLATFORM == "linux":
        redis_queue_name = common_config.REDIS_LINUX_TASKS
    elif PLATFORM == "windows" or PLATFORM == "win32":
        redis_queue_name = common_config.REDIS_WINDOWS_TASKS
    else:
        print(PLATFORM)
        log.error(f"Error. Do not support this platform: [{PLATFORM}]")
        raise RuntimeError

    redis_conn = redis.Redis(connection_pool=use_redis_pool)
    try:
        task_info_str = redis_conn.lpop(redis_queue_name).decode("utf-8")
    except AttributeError:
        log.debug("There is no wait task in the redis...")
        return None
    else:
        log.info(f"Get a task: {task_info_str}")

        re_id = re.compile("[0-9]+")
        re_status = re.compile("[a-zA-Z]+")

        task_id = re_id.search(task_info_str).group()
        task_status = re_status.search(task_info_str).group()

        return {"id": task_id, "status": task_status}
