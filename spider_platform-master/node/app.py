import sys
from flask import Flask
from flask_restful import Api, Resource
from flask_apscheduler import APScheduler

from node.db.exts import db
from node.config.app_config import config
from node.resource import TaskControl, AliveCheck

from node.core.update_info import check_if_self_is_a_main_process
from common.common_config import QUERY_NODE_STATUS_URL, TASK_STOP_URL
from common.log import log

import inspect

PLATFORM = sys.platform
scheduler = APScheduler()


def create_app(start_type):
    app = Flask(__name__)
    print(f"Create app with start type: {start_type}.")
    log.info(f"Create app with start type: {start_type}.")
    app.config.from_object(config[start_type])
    config[start_type].init_app(app)

    print(f"Check the app db uri: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    log.debug(f"Check the app db uri: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    is_deploy = False
    previous_frame = inspect.currentframe().f_back
    for i in range(10):
        previous_frame = previous_frame.f_back
        try:
            (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
        except AttributeError:
            break
        else:
            log.debug(f"i: {i} {filename, line_number, function_name, lines, index}")
            if lines is not None:
                if function_name == "locate_app":
                    log.info("This process is deploy.")
                    is_deploy = True
                    break
                else:
                    log.info("This process is start server.")
                    break

    if check_if_self_is_a_main_process(start_type) and not is_deploy:
        db.init_app(app)
        api = Api(app)
        api.add_resource(HelloWorld, '/')
        api.add_resource(TaskControl, TASK_STOP_URL.split("?")[0])
        api.add_resource(AliveCheck, QUERY_NODE_STATUS_URL)

        log.debug(f"Start a new scheduler")
        scheduler.init_app(app)
        scheduler.start()

    return app


class HelloWorld(Resource):
    hello = {'hello': 'world'}

    def get(self):
        return self.hello
