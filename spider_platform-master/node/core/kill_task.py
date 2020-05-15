import time
from common.log import log

from common.common_config import TASK_STATUS_INTERRUPT
from node.core.global_parameter import current_task_list
from node.core.update_info import update_the_task_status, update_time_info_for_the_task, update_node_info


def kill_task_with_task_id(task_id):
    try:
        target_task = current_task_list[task_id]
    except KeyError:
        log.error(f"The task[{task_id}] is not running.")
        print(f"The task[{task_id}] is not running.")
        return False
    else:
        target_task.terminate()
        # time.sleep(0.5)

    task_status = target_task.is_alive()
    if not task_status:
        log.info(f"Success stop task[{task_id}] with terminate signal.")
        print(f"Success stop task[{task_id}] with terminate signal.")
        current_task_list.pop(task_id)
        update_the_task_status(task_id, TASK_STATUS_INTERRUPT)
        update_time_info_for_the_task(task_id, "end_time")
        update_node_info("cur_ps", len(current_task_list))
        # update_task_task_in_db(task_id, TASK_STATUS_FINISHED)
        return True
    else:
        log.warning(f"Failed to stop task[{task_id}]. retry with kill signal.")
        target_task.kill()
        # time.sleep(0.5)

        task_status = target_task.is_alive()
        if not task_status:
            log.info(f"Success stop task[{task_id}] with kill signal.")
            print(f"Success stop task[{task_id}] with kill signal.")
            current_task_list.pop(task_id)
            update_the_task_status(task_id, TASK_STATUS_INTERRUPT)
            update_time_info_for_the_task(task_id, "end_time")
            update_node_info("cur_ps", len(current_task_list))
            # update_task_task_in_db(task_id, TASK_STATUS_FINISHED)
            return True
        else:
            log.error(f"Failed to stop task[{task_id}] with terminate and kill.")
            print(f"Failed to stop task[{task_id}] with terminate and kill.")
            return False
