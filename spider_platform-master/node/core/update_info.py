import os
from flask import Flask
from node.config.app_config import config

from common import log
from common.models import SpiderTask, Node
from common.common_config import NODE_STATUS_INVALID, NODE_STATUS_NORMAL

from datetime import datetime
from node.db.exts import db

from node.core.get_self_info import generate_node_info
from node.core.global_parameter import node_running_info
from node.core.send_message import delete_node, get_main_node_host
from node.core.get_self_info import get_host_ip
from sqlalchemy.exc import ProgrammingError, DataError, IntegrityError


def create_app(start_type):
    log.info("Create an app just for db.")
    print("Create an app just for db.")
    app = Flask(__name__)
    app.config.from_object(config[start_type])
    config[start_type].init_app(app)
    print(app.config.get("SQLALCHEMY_DATABASE_URI"))
    db.init_app(app)

    return app


def update_node_running_info():
    node_info = generate_node_info()
    node_running_info.update(node_info)


def check_if_self_is_a_main_process(start_type):
    flask_app = create_app(start_type)
    flask_context = flask_app.app_context()
    flask_context.push()

    self_ip = get_host_ip()
    ppid = os.getppid()
    node_list = db.session.query(Node).filter(Node.ip_addr == self_ip, Node.ps_id == ppid,
                                              Node.status == NODE_STATUS_NORMAL).all()
    log.info(f"Current ppid: {ppid}, selected node list: {node_list}")
    flask_context.pop()
    if len(node_list) > 0:
        return False
    else:
        return True


def delete_the_node_info_conflict_with_me():

    self_ip = get_host_ip()
    node_list = db.session.query(Node).filter(Node.ip_addr == self_ip).all()
    main_node_host = get_main_node_host()

    if len(node_list) == 0:
        return
    else:
        for node in node_list:
            res = delete_node(main_node_host, node.id)
            if res["ret"] == "success":
                log.info(f"Success delete node: {node.id}")
            else:
                log.error(f"Failed to delete node: {node.id}")


def update_invalid_node_status():
    # flask_app = create_app('development')
    # flask_context = flask_app.app_context()
    # flask_context.push()

    self_ip = get_host_ip()
    node_list = db.session.query(Node).filter(Node.ip_addr == self_ip).all()

    if len(node_list) == 0:
        # flask_context.pop()
        return
    else:
        for node in node_list:
            Node.query.filter_by(id=node.id).update({"status": NODE_STATUS_INVALID})
            try:
                db.session.commit()
            except ProgrammingError as e:
                log.error(e)
            except IntegrityError as e:
                db.session.rollback()
                log.error(e)
            except DataError as e:
                log.error(e)
            else:
                log.info(f"Update the node[{node.id}]'s status to {NODE_STATUS_INVALID}")

    # flask_context.pop()


def update_node_info(field, value):
    # flask_app = create_app('development')
    # flask_context = flask_app.app_context()
    # flask_context.push()

    node_id = node_running_info["node_id"]
    Node.query.filter_by(id=node_id).update({field: value})

    try:
        db.session.commit()
    except ProgrammingError as e:
        log.error(e)
    except IntegrityError as e:
        db.session.rollback()
        log.error(e)
    except DataError as e:
        log.error(e)
    else:
        log.info(f"Update node info: node_id: {node_id}, field: {field}, value: {value}")
        print(f"Update node info: node_id: {node_id}, field: {field}, value: {value}")
    finally:
        pass
        # flask_context.pop()


def update_task_info(task_id, field, value):
    # flask_app = create_app('development')
    # flask_context = flask_app.app_context()
    # flask_context.push()

    SpiderTask.query.filter_by(id=task_id).update({field: value})

    try:
        db.session.commit()
    except ProgrammingError as e:
        log.error(e)
    except IntegrityError as e:
        db.session.rollback()
        log.error(e)
    except DataError as e:
        log.error(e)
    else:
        log.info(f"Update spider_task: id: {task_id}, field: {field}, value: {value}")
        print(f"Update spider_task: id: {task_id}, field: {field}, value: {value}")
    finally:
        pass
        # flask_context.pop()


def upload_this_node_info():
    # flask_app = create_app('development')
    # flask_context = flask_app.app_context()
    # flask_context.push()

    # delete_the_node_info_conflict_with_me()
    node_info = generate_node_info()

    info_db = Node(ip_addr=node_info.get("ip_addr", None), host_name=node_info.get("host_name", None),
                   node_type=node_info.get("node_type", None), max_ps=node_info.get("max_ps", 10),
                   cur_ps=node_info.get("cur_ps", 0), status=node_info.get("status", 0),
                   ps_id=node_info.get("ps_id", 0))

    db.session.add(info_db)
    try:
        db.session.commit()
    except ProgrammingError as e:
        log.error(e)
    except IntegrityError as e:
        db.session.rollback()
        log.error(e)
    except DataError as e:
        log.error(e)
    else:
        print(f"Get the node id: {info_db.id}")
        log.info(f"Upload new node id: {info_db.id}")
        node_running_info.update({"node_id": info_db.id})
        print(node_running_info)
    finally:
        pass
        # flask_context.pop()


def update_the_task_status(task_id, status):
    # flask_app = create_app('development')
    # flask_context = flask_app.app_context()
    # flask_context.push()

    task = SpiderTask.query.get_or_404(task_id)
    task.status = status

    db.session.add(task)
    try:
        db.session.commit()
    except ProgrammingError as e:
        log.error(e)
    except IntegrityError as e:
        db.session.rollback()
        log.error(e)
    except DataError as e:
        log.error(e)
    else:
        log.info(f"Update task[{task_id}] status to [{status}]")
    finally:
        pass
        # flask_context.pop()


def update_time_info_for_the_task(task_id, time_type):
    # flask_app = create_app('development')
    # flask_context = flask_app.app_context()
    # flask_context.push()

    time_str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    SpiderTask.query.filter_by(id=task_id).update({time_type: time_str})

    try:
        db.session.commit()
    except ProgrammingError as e:
        log.error(e)
    except IntegrityError as e:
        db.session.rollback()
        log.error(e)
    except DataError as e:
        log.error(e)
    else:
        log.info(f"Update task[{task_id}]'s {time_type} to {time_str}")
    finally:
        pass
        # flask_context.pop()
