from node.app import scheduler

from node.core.update_info import update_invalid_node_status
from node.core.update_info import upload_this_node_info
from node.core.update_info import update_node_running_info

from common.log import log


def upload_node_information():
    with scheduler.app.app_context():
        log.debug("Start maintain node information.")
        update_invalid_node_status()
        upload_this_node_info()
        update_node_running_info()
