import json
import requests

from common import log
from common.common_config import ERROR_RET_CANNOT_CONNECT_NODE, NODE_DROP_URL, EXPORT_FILE_URL

from node.core.global_parameter import node_running_info


def delete_node(main_node_host, node_id):
    """
        向调度节点发送请求删除对应节点信息
    """
    url = main_node_host + NODE_DROP_URL.format(node_id=node_id)
    try:
        response = requests.get(url)
    except Exception as e:
        log.error("节点通信失败 error: {}".format(str(e)))
        return ERROR_RET_CANNOT_CONNECT_NODE
    else:
        return json.loads(response.text)


def export_file(main_node_host, task_id):
    """
                向调度节点发送请求导出结果至文件
    """
    url = main_node_host + EXPORT_FILE_URL.format(task_id=task_id)
    try:
        response = requests.get(url)
    except Exception as e:
        log.error("节点通信失败 error: {}".format(str(e)))
        return ERROR_RET_CANNOT_CONNECT_NODE
    else:
        return json.loads(response.text)


def get_main_node_host():
    try:
        main_node = node_running_info["main_node_host"]
    except KeyError:
        log.error("Failed to get main node ip.")
        raise RuntimeError
    else:
        return main_node


def let_the_main_node_export_result_to_file(task_id):
    main_node_host = get_main_node_host()
    log.info(f"send message for export file of task[{task_id}]")

    res = export_file(main_node_host, task_id)
    if res["ret"] == "success":
        log.info(f"Success export file: {task_id}")
    else:
        log.error(f"Failed to export file: {task_id}")
