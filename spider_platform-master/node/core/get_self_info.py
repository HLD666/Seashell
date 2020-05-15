import os
import sys
import socket
import multiprocessing

from common.common_config import NODE_STATUS_NORMAL
from common.log import log
from node.core.global_parameter import current_task_list
from node.config.task_config import MAX_CONCURRENT_TASK


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        print(e)
        return None
    else:
        return ip
    finally:
        s.close()


def get_host_name():
    return socket.getfqdn(socket.gethostname())


def get_platform_type():
    return sys.platform


def get_cpu_count():
    return multiprocessing.cpu_count()


def get_current_task_number():
    return len(current_task_list)


def get_pid():
    return os.getpid()


def generate_node_info():
    ip = get_host_ip()
    host_name = get_host_name()
    platform_type = get_platform_type()
    cur_ps = get_current_task_number()
    ps_id = get_pid()

    if MAX_CONCURRENT_TASK is not None:
        max_ps = MAX_CONCURRENT_TASK
    else:
        max_ps = get_cpu_count()

    node_info = {"ip_addr": ip, "host_name": host_name,
                 "node_type": platform_type, "max_ps": int(max_ps),
                 "cur_ps": cur_ps, "status": NODE_STATUS_NORMAL,
                 "ps_id": ps_id}
    log.info(f"Get node info: {node_info}")

    return node_info


if __name__ == "__main__":
    my_ip = get_host_ip()
    print(my_ip)

    my_host_name = get_host_name()
    print(my_host_name)

    platform = get_platform_type()
    print(platform)

    cpu_count = get_cpu_count()
    print(cpu_count)
