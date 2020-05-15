"""
封装的数据库操作，都是具体页面会用到的
"""
from common.models import *
from common.models import db
from common import log
from common.common_config import HOT_WEBSITE_COUNT


def query_hot_website():
    return Website.query.filter_by(is_hot=1).limit(HOT_WEBSITE_COUNT)


def query_search_website(keyword):
    return Website.query.filter(Website.name.like("%" + keyword + "%")).all()


def query_category_website(category_id):
    return Website.query.filter_by(category_id=category_id).all()


def query_single_website(website_id):
    return Website.query.get(website_id)


def query_categorys():
    return Category.query.all()


def query_single_category(category_id):
    return Category.query.get(category_id)


def query_website_template(website_id):
    return SpiderTemplate.query.filter_by(website_id=website_id).all()


def query_single_template(template_id):
    return SpiderTemplate.query.get(template_id)


def query_template_description(template_id):
    return TemplateDescription.query.get(template_id)


def query_template_fileds(template_id):
    return TemplateFileds.query.filter_by(template_id=template_id).order_by('inner_id').all()


def query_template_paras(template_id):
    return TemplateParas.query.filter_by(template_id=template_id).order_by('inner_id').all()


def query_template_example(template_id):
    return TemplateDataExample.query.get(template_id)


def query_example(table_name, fileds, limit=10):
    sql_str = "select " + str(fileds).replace("[", "").replace("]", "").replace("'", "") + " from data_res." \
              + table_name + ' limit ' + str(limit)
    return list(db.session.execute(sql_str))


def query_para_file(file_id):
    return ParaFiles.query.get(file_id)


def query_tasks():
    return SpiderTask.query.order_by('id').all()


def query_timing_task():
    return SpiderTask.query.filter_by(is_timing=1).all()


def query_single_task(task_id):
    return SpiderTask.query.get(task_id)


def query_task_count(**condition):
    if condition is None:
        return SpiderTask.query.count()
    else:
        return SpiderTask.query.filter_by(**condition).count()


def update_task(task_id, field, value):
    SpiderTask.query.filter_by(id=task_id).update({field: value})
    db.session.commit()


def update_node_task(node_id, field, value):
    SpiderTask.query.filter_by(node_id=node_id).update({field: value})
    db.session.commit()


def update_template(template_id, field, value):
    SpiderTemplate.query.filter_by(id=template_id).update({field: value})
    db.session.commit()


def db_delete_task(task_id):
    SpiderTask.query.filter_by(id=task_id).delete()
    db.session.commit()


def query_nodes():
    return Node.query.order_by('id').all()


def db_delete_node(node_id):
    Node.query.filter_by(id=node_id).delete()
    db.session.commit()
    log.critical("Node {} 被删除".format(node_id))


def query_single_node(node_id):
    return Node.query.get(node_id)


def query_nodes_count():
    return Node.query.count()


def query_running_node_count():
    return Node.query.filter_by(status=1).count()


def query_res_by_fields(table_name, fields):
    sql_str = "select " + str(fields).replace('[','').replace(']','').replace("'", "") + " from data_res." + table_name
    return db.session.execute(sql_str)
