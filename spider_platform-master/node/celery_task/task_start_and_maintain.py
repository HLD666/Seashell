import time
from flask import g
from common.log import log
from node.start_app import celery_app


@celery_app.task()
def task_monitor():
    try:
        current_task_list = g.cur_ps
    except AttributeError:
        log.warning("There is no running task.")
    else:
        for task in current_task_list:
            task_handel = task["handel"]


@celery_app.task()
def implement_task():
    # spider.start(db, task_info["table"])
    time.sleep(6)
    print("spider finished, ok.")
    return 0
