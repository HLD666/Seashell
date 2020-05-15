from flask_restful import Resource
from flask import jsonify, request
from node.core.get_self_info import generate_node_info
from node.core.kill_task import kill_task_with_task_id

from common.common_config import SUCCESS_RET_STOP_TASK, ERROR_RET_STOP_TASK, NODE_STATUS_NORMAL
from common.log import log


class TaskControl(Resource):

    @classmethod
    def get(cls):
        task_id = request.args.get('task_id', 0, type=int)
        operation = request.args.get('operation', 'stop', type=str)

        log.info(f"Stop task_id:{task_id}, operation: {operation}")
        print(f"Stop task_id:{task_id}, operation: {operation}")

        if operation == "stop":
            # task = current_task_list[task_id]
            flag = kill_task_with_task_id(task_id)
            if flag:
                return jsonify(SUCCESS_RET_STOP_TASK)
            else:
                return jsonify(ERROR_RET_STOP_TASK)


class AliveCheck(Resource):

    def __init__(self):
        self.node_info = generate_node_info()
        self.node_info.update({"node_status": NODE_STATUS_NORMAL})

    def get(self):
        return jsonify(self.node_info)
