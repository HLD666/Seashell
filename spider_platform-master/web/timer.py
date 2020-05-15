import time
import redis
import requests
import json
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from threading import Thread
from configs import SCAN_INTERVAL, DB_URI
from exts import redis_pool
from common.common_config import *
from common import log


engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class SpiderTask(Base):
    __tablename__ = 'spider_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    template_id = Column(Integer)
    task_type = Column(Integer)
    is_timing = Column(Integer)
    publish_time = Column(DateTime)
    user = Column(String(50))
    execute_cycle = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Integer)
    node_id = Column(Integer)
    paras_table = Column(String(100))
    res_table = Column(String(100))
    res_file = Column(String(100))


class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_addr = Column(String(50))
    host_name = Column(String(50))
    node_type = Column(String(50))
    max_ps = Column(Integer)
    cur_ps = Column(Integer)
    status = Column(Integer)
    ps_id = Column(Integer)


def query_timing_task():
    return session.query(SpiderTask).filter_by(is_timing=1).all()


def query_single_task(task_id):
    return session.query(SpiderTask).get(task_id)


def create_res_table(task_id):
    template_id = query_single_task(task_id).template_id
    table_template = 'data_example_' + str(template_id)
    table_name = 'res_' + str(task_id) + "_" + str(int(time.time()))
    sql_str = "create table data_res." + table_name + " ( select * from data_res." + table_template + " where 1>2)"

    session.execute(sql_str)
    session.commit()

    return table_name


def update_task(task_id, field, value):
    session.query(SpiderTask).filter_by(id=task_id).update({field: value})
    session.commit()


def update_node_task(node_id, field, value):
    session.query(SpiderTask).filter_by(node_id=node_id).update({field: value})
    session.commit()


def query_nodes():
    nodes = session.query(Node).all()
    session.commit()
    return nodes


def delete_node(node_id):
    session.query(Node).filter_by(id=node_id).delete()
    session.commit()
    log.critical("Node {} 被删除".format(node_id))


def update_node(node_id, field, value):
    session.query(Node).filter_by(id=node_id).update({field: value})
    session.commit()


def str_to_tiem_stamp(time_str):
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_array))


def remove_node(node_id):
    update_node_task(node_id, 'status', TASK_STATUS_INTERRUPT)
    update_node_task(node_id, 'node_id', None)
    delete_node(node_id)


class TaskTimer(Thread):
    def __init__(self):
        self.interval = SCAN_INTERVAL
        Thread.__init__(self, name="Task timer")

    def run(self):
        while True:
            time.sleep(self.interval)
            tasks = query_timing_task()
            for task in tasks:
                if task.status not in [TASK_STATUS_FINISHED, TASK_STATUS_INTERRUPT]:
                    continue

                cur_time = int(time.time())
                start_time = str_to_tiem_stamp(str(task.start_time))
                peroid = int(task.execute_cycle)
                if cur_time - start_time < peroid:
                    continue

                redis_conn = redis.Redis(connection_pool=redis_pool)
                if task.task_type == TASK_RUN_TYPE_LINUX:
                    redis_conn.lpush(REDIS_LINUX_TASKS, str((task.id, "start")))
                elif task.task_type == TASK_RUN_TYPE_WINDOWS:
                    redis_conn.lpush(REDIS_WINDOWS_TASKS, str((task.id, "start")))
                else:
                    log.error("定时任务类型错误")
                    continue

                table_name = create_res_table(task.id)
                update_task(task.id, "res_table", table_name)
                update_task(task.id, "status", TASK_STATUS_PREPARING)
                log.critical("定时任务 {} 启动".format(task.id))

            nodes = query_nodes()
            for node in nodes:
                if node.status == NODE_STATUS_INVALID:
                    remove_node(node.id)
                    continue

                url = 'http://' + node.ip_addr + ':5000' + QUERY_NODE_STATUS_URL
                try:
                    response = requests.get(url=url, timeout=10)
                    ret = json.loads(response.text)
                    if ret['status'] == NODE_STATUS_NORMAL:
                        log.critical("Node {} is OK!".format(str(node.id)))
                        if node.status == NODE_STATUS_DISCONNECT:
                            update_node(node.id, 'status', NODE_STATUS_NORMAL)
                except Exception as e:
                    if node.status == NODE_STATUS_NORMAL:
                        update_node(node.id, 'status', NODE_STATUS_DISCONNECT)
                        log.critical("Node {} is disconnect! error={}".format(str(node.id), str(e)))
                        continue

                    log.error("Node {} error={}".format(node.id, str(e)))
