import importlib
from multiprocessing import Process

from common import log
from common.common_config import TASK_STATUS_RUNNING
from node.core.global_parameter import current_task_list, node_running_info
from node.core.update_info import update_the_task_status, update_time_info_for_the_task, update_task_info


def get_the_task_info_from_register_list(template_id, task_list):
    task_location = task_list.get(template_id, (None, None))
    task_location_info = {"file_path": task_location[0], "class_name": task_location[1]}

    return task_location_info


def start_task_use_multiprocess(spider, task_id):
    spider_task = Process(target=spider.start)
    spider_task.start()

    task_status = spider_task.is_alive()
    if task_status:
        log.info(f"Success start a new task[{task_id}].")
        current_task_list.update({task_id: spider_task})
        update_the_task_status(task_id, TASK_STATUS_RUNNING)
        update_time_info_for_the_task(task_id, "start_time")
        update_task_info(task_id, "end_time", None)

        node_id = node_running_info["node_id"]
        update_task_info(task_id, "node_id", node_id)
    else:
        print(f"Failed to start task: {task_id}")
        log.error(f"Failed to start task: {task_id}")
        spider_task.kill()


def start_the_task_with_task_info(task_info):
    try:
        task_module = importlib.import_module(task_info["file_path"], package=__package__)
    except AttributeError:
        log.error(f"Can't find the task code in local. [{task_info['file_path']}]")
    else:
        log.debug(f"Start module: {task_info['file_path']}.{task_info['class_name']}")
        print(f"Start module: {task_info['file_path']}.{task_info['class_name']}")
        task_args = (task_info["template"], task_info["paras_table"], task_info["res_table"])
        print(f"task args: {task_args}")

        spider = eval(f"task_module.{task_info['class_name']}{task_args}")
        log.debug(f"eval: task_module.{task_info['class_name']}{task_args}")
        log.info(f"start task[{task_info['id']}].")
        # spider.start(db, task_info["table"])
        # task = subprocess.run([spider.task, db, task_info["table"]])
        # g.cur_ps.update({task_info["id"]: {"handel": task}})
        # implement_task.delay()

        start_task_use_multiprocess(spider, task_info["id"])
        # spider_task = Process(target=spider.start)
        # spider_task.start()
        # put_task_into_flask_g(spider_task, task_info["id"])

        log.info(f"finished start task[{task_info['id']}].")
