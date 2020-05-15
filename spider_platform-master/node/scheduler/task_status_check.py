import copy
from node.app import scheduler

from common.log import log
from common.common_config import TASK_STATUS_FINISHED, TASK_STATUS_INTERRUPT

from node.core.global_parameter import current_task_list, node_running_info
from node.core.update_info import update_the_task_status, update_time_info_for_the_task, update_node_info
from node.core.send_message import let_the_main_node_export_result_to_file


def update_current_task_status():
    with scheduler.app.app_context():
        log.debug("Start maintain running task.")
        print(f"Running task: {current_task_list}")
        log.info(f"Running task: {current_task_list}")
        task_list = copy.copy(current_task_list)
        for task_id, task in task_list.items():
            task_status = task.is_alive()
            if task_status is not True:
                exit_code = task.exitcode
                if exit_code == 0:
                    log.info(f"Task[{task_id}] normally finished. exit code:[{exit_code}]")
                    update_the_task_status(task_id, TASK_STATUS_FINISHED)
                    let_the_main_node_export_result_to_file(task_id)
                else:
                    log.info(f"Task[{task_id}] not normally finished. exit code:[{exit_code}]")
                    update_the_task_status(task_id, TASK_STATUS_INTERRUPT)
                    let_the_main_node_export_result_to_file(task_id)

                update_time_info_for_the_task(task_id, "end_time")
                current_task_list.pop(task_id)

        update_node_info("cur_ps", len(current_task_list))
        node_running_info.update({"cur_ps": len(current_task_list)})
        # print(f"pid: {os.getpid()}, ppid:{os.getppid()}, node_id:{node_running_info}")
