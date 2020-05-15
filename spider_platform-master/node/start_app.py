#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    Start a flask app to load spider task.

    sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
"""
import os
import atexit
import copy
import sys
sys.path.append("..")

from common.log import log
from node.app import create_app
from node.core.kill_task import kill_task_with_task_id
from node.core.global_parameter import current_task_list

from node.config import db_config
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

flask_app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# celery_app = make_celery(flask_app)


@atexit.register
def perform_the_exit_func():
    # update all the task status
    task_list = copy.copy(current_task_list)
    for task_id in task_list.keys():
        kill_task_with_task_id(task_id)

    print(f"Process normally exit. pid[{os.getpid()}]")
    log.info(f"Process normally exit. pid[{os.getpid()}]")


@flask_app.cli.command()
def deploy():
    pass


if __name__ == '__main__':
    # get self node information
    # upload_this_node_info()
    # deploy("development")
    flask_app.run(debug=False, use_reloader=False, host="0.0.0.0")

    # start celery server
    # celery_start_argv = ['worker', '-B', '-s', 'celery_schedule_bak/celery_schedule']
    # celery_start_argv = ['beat', '-s', 'celery_schedule_bak/celery_schedule']
    # celery_process = Process(target=celery_app.worker_main, args=(celery_start_argv,))
    # celery_process.start()
    # celery_app.close()

    # celery_cmdline = ["celery", "-A", "app", "beat"]
    # celery_process = subprocess.Popen(celery_cmdline, shell=True)

    # start flask server
    # flask_process = Process(target=flask_app.run, kwargs={'debug': True})
    # flask_process.start()
    # app.run(debug=True)

    # time.sleep(4)
    # celery_process.kill()
    # from node.celery_task.task_read_redis import start_task
    # node_task_process = Process(target=start_task.delay, args=(5,))
    # node_task_process.start()

    # celery_process.join()
    # node_task_process.join()
    # flask_process.join()
    # celery_process.wait()
