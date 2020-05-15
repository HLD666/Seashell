import csv
import time
import redis
import json
import requests
import chardet
from exts import redis_pool
from sql_operation import *
from configs import UPLOAD_FOLDER
from datetime import datetime
from common.common_config import *
from common import log


def check_headers(mapping, headers):
    """
    检查文件的表头和所需的表头是否一致
    """
    filed_list = list()
    target = mapping.keys()
    if len(target) != len(headers):
        return False, None

    for header in headers:
        if header not in target:
            return False, None
        filed_list.append(mapping[header])

    return True, filed_list


def create_para_table(template_id):
    """
    创建爬虫输入参数数据库表
    """
    table_template = 'para_example_' + str(template_id)
    table_name = "para_" + str(template_id) + "_" + str(int(time.time()))
    sql_str = "create table data_res." + table_name + " ( select * from data_res." + table_template + " where 1>2)"

    db.session.execute(sql_str)
    db.session.commit()

    return table_name


def put_para_row(table_name, field_list, row):
    """
    将文件中的每一行都放入到数据库中
    """
    sql_str = "insert into data_res." + table_name + " (" + str(field_list).replace("[", "").replace("]", "").\
        replace("'", "") + ") values (" + str(row).replace("[", "").replace("]", "") + ")"
    print("######### " + str(sql_str))
    db.session.execute(sql_str)
    db.session.commit()


def create_res_table(task_id):
    """ 创建结果表 """
    template_id = query_single_task(task_id).template_id
    table_template = 'data_example_' + str(template_id)
    table_name = 'res_' + str(task_id) + "_" + str(int(time.time()))
    sql_str = "create table data_res." + table_name + " ( select * from data_res." + table_template + " where 1>2)"

    db.session.execute(sql_str)
    db.session.commit()

    return table_name


def get_encoding(file_name):
    with open(file_name, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def create_task(post_data):
    """
    创建任务流程，将用户上传的参数文件中的数据保存到数据库中，根据post过来的数据创建数任务
    """
    file_id = post_data['paraFileId']
    template_id = post_data['templateId']
    para_file = UPLOAD_FOLDER + "/" + query_para_file(file_id).file_name

    rows = query_template_paras(template_id)
    headers_mapping = dict()
    for row in rows:
        if row.para_name != 'example':
            headers_mapping[row.para_cn_name] = row.para_name

    with open(para_file, encoding=get_encoding(para_file)) as csv_file:
        reader = csv.reader(csv_file)
        table_name = create_para_table(template_id)
        for index, row in enumerate(reader):
            if index == 0:
                res, field_list = check_headers(headers_mapping, row)
                if not res:
                    return ERROR_RET_UPLOAD_FILE_ERROR

            else:
                put_para_row(table_name, field_list, row)

    name = post_data['taskName']
    if post_data['taskType'] == TASK_TIMING_TYPE_CYCLE:
        is_timing = 1
        execute_cycle = post_data['period']
    else:
        is_timing = 0
        execute_cycle = 0
    publish_time = datetime.now()
    template = query_single_template(template_id)

    task = SpiderTask(name=name, template_id=template_id, is_timing=is_timing, status=TASK_STATUS_INIT,
                      execute_cycle=execute_cycle, publish_time=publish_time, paras_table=table_name,
                      task_type=template.task_type, node_type=template.node_type)
    db.session.add(task)
    db.session.commit()

    return SUCCESS_RET_CREATE_TASK


def start_task(task_id, node_type):
    """
    启动任务，将任务放进redis中，并跟新任务状态
    """
    table_name = create_res_table(task_id)
    update_task(task_id, "res_table", table_name)

    redis_conn = redis.Redis(connection_pool=redis_pool)
    if node_type == TASK_RUN_TYPE_LINUX:
        redis_conn.lpush(REDIS_LINUX_TASKS, str((task_id, "start")))
    elif node_type == TASK_RUN_TYPE_WINDOWS:
        redis_conn.lpush(REDIS_WINDOWS_TASKS, str((task_id, "start")))
    else:
        return ERROR_RET_UNKNOWN_TASK_TYPE

    update_task(task_id, "status", TASK_STATUS_PREPARING)
    return SUCCESS_RET_START_TASK


def stop_task(cur_task):
    """
    定制任务，由调度核心发向执行节点发送停止请求
    """
    node_id = cur_task.node_id
    node = query_single_node(node_id)
    url = 'http://' + node.ip_addr + ':5000' + TASK_STOP_URL.format(task_id=str(cur_task.id))
    try:
        response = requests.get(url)
        return json.loads(response.text)
    except Exception as e:
        log.error("节点通信失败 error: {}".format(str(e)))
        return ERROR_RET_CANNOT_CONNECT_NODE


def delete_task(cur_task):
    """ 任务删除，首先是停止，然后从数据库中删除 """
    try:
        stop_task(cur_task)
    except Exception as e:
        log.error("停止任务错误： {}".format(str(e)))
    db_delete_task(cur_task.id)
    return SUCCESS_RET_DELETE_TASK

