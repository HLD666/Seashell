"""
----------------------------------------数据库定义模块-------------------------------------------------------------------
继承自model，定义数据库表字段和数据库表之前的关联关系
"""

import inspect

previous_frame = inspect.currentframe().f_back

for i in range(20):
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
    if lines is not None:
        if "node" in filename:
            from node.db.exts import db
            break
        elif "web" in filename:
            from web.exts import db
            break
        else:
            raise RuntimeError
    else:
        previous_frame = previous_frame.f_back
else:
    raise RuntimeError


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))


class Website(db.Model):
    __tablename__ = 'website'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    is_hot = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class SpiderTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    para_file = db.Column(db.String(50))
    node_type = db.Column(db.String(50))
    task_type = db.Column(db.String(50))
    sctript_name = db.Column(db.String(100))


class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_addr = db.Column(db.String(50))
    host_name = db.Column(db.String(50))
    node_type = db.Column(db.String(50))
    max_ps = db.Column(db.Integer)
    cur_ps = db.Column(db.Integer)
    status = db.Column(db.Integer)
    ps_id = db.Column(db.Integer)


class SpiderTask(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    template_id = db.Column(db.Integer, db.ForeignKey('spider_template.id'))
    node_type = db.Column(db.Integer)
    task_type = db.Column(db.Integer)
    script_name = db.Column(db.String(200))
    is_timing = db.Column(db.Integer)
    publish_time = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    execute_cycle = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    paras_table = db.Column(db.String(100))
    res_table = db.Column(db.String(100))
    res_file = db.Column(db.String(100))


class TemplateDescription(db.Model):
    template_id = db.Column(db.Integer, db.ForeignKey('spider_template.id'), primary_key=True)
    description = db.Column(db.String(1000))


class TemplateFileds(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    template_id = db.Column(db.Integer, db.ForeignKey('spider_template.id'))
    inner_id = db.Column(db.Integer)
    filed_name = db.Column(db.String(50))
    filed_cn_name = db.Column(db.String(50))
    filed_preview_type = db.Column(db.String(50))
    filed_string = db.Column(db.String(1000))
    filed_image = db.Column(db.String(100))
    filed_table = db.Column(db.String(100))


class TemplateParas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    template_id = db.Column(db.Integer, db.ForeignKey('spider_template.id'))
    inner_id = db.Column(db.Integer)
    para_name = db.Column(db.String(50))
    para_cn_name = db.Column(db.String(50))
    para_preview_type = db.Column(db.String(50))
    para_string = db.Column(db.String(1000))
    para_image = db.Column(db.String(100))
    para_table = db.Column(db.String(100))


class TemplateDataExample(db.Model):
    template_id = db.Column(db.Integer, db.ForeignKey('spider_template.id'), primary_key=True)
    example_table = db.Column(db.String(50))


class ParaFiles(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    file_name = db.Column(db.String(200))
    create_time = db.Column(db.DateTime)
