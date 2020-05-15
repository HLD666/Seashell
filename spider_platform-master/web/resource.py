"""
此文件定义Rest资源的返回类，与对应的URL绑定，当URL被请求时，相关资源类会被调用，返回对应数据
"""
import os
import csv
import json
from datetime import datetime
from uuid import uuid1
from flask import request, send_from_directory
from flask_restful import Resource
from math import ceil
from sql_operation import *
from core import create_task, start_task, stop_task, delete_task
from configs import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, IMAGE_FOLDER, URL_PRIFIX
from common.common_config import *
from common import log


class HomePage(Resource):
    """
    Home页面资源，主要有热门站点和站点种类两个数据
    """
    def get(self):
        hot_website = list()
        rows = query_hot_website()
        for row in rows:
            website_id = row.id
            hot_website.append({
                'websiteName': row.name,
                'websiteUrl': URL_PRIFIX + '/create?website_id={}'.format(website_id),
                'logoUrl': URL_PRIFIX + '/image/website_logo?website_id={}'.format(website_id),
                'websiteId': website_id
            })

        categorys = list()
        rows = query_categorys()
        for row in rows:
            category_id = row.id
            categorys.append({
                'cateName': row.name,
                'cateUrl': URL_PRIFIX + '/category?category_id={}'.format(category_id),
                'categoryId': category_id
            })

        res = {
            'hotWebsite': hot_website,
            'websiteCategorys': categorys
        }

        return res


class SearchPage(Resource):
    """
    搜索返回页面资源，返回对关键字的搜索结果
    """
    def get(self):
        page_size = 10
        keyword = request.args.get('keyword')
        # 输入关键字为空的时候，返回空数据
        if not keyword:
            return {
                "currentPage": 1,
                "totalPage": 0,
                "websiteList": []
            }
        page = request.args.get('page')
        if not page:
            page = 1
        page = int(page)
        start = (page - 1) * page_size
        end = page * page_size

        websites = list()
        rows = query_search_website(keyword)
        totol_page = ceil(len(rows) / page_size)
        rows = rows[start:end]
        for row in rows:
            website_id = row.id
            websites.append({
                'websiteName': row.name,
                'websiteUrl': URL_PRIFIX + '/create?website_id={}'.format(website_id),
                'logoUrl': URL_PRIFIX + '/image/website_logo?website_id={}'.format(website_id),
                'description': row.description,
                'websiteId': website_id
            })

        res = {
            "currentPage": page,
            "totalPage": totol_page,
            "websiteList": websites
        }
        return res


class CategoryPgae(Resource):
    """
    分类返回页面资源，返回某个种类下的站点
    """
    def get(self):
        page_size = 10
        category_id = request.args.get('category_id')
        if not category_id:
            return ERROR_RET_NO_PARAS

        page = request.args.get('page')
        if not page:
            page = 1
        page = int(page)
        start = (page - 1) * 10
        end = page * 10

        category = query_single_category(category_id)
        if not category:
            return ERROR_RET_INVALID_PARAS

        crumbs = [
            {
                "title": "首页",
                "linkUrl": URL_PRIFIX + "/home"
            },
            {
                "title": category.name,
                "linkUrl": URL_PRIFIX + "/category?category_id={}".format(category_id)
            }
        ]

        websites = list()
        if not category_id:
            return []

        rows = query_category_website(category_id)
        totol_page = ceil(len(rows) / page_size)
        rows = rows[start:end]
        for row in rows:
            website_id = row.id
            websites.append({
                'websiteName': row.name,
                'websiteUrl': URL_PRIFIX + '/create?website_id={}'.format(website_id),
                'logoUrl': URL_PRIFIX + '/image/website_logo?website_id={}'.format(website_id),
                'description': row.description,
                'websiteId': website_id
            })

        res = {
            "crumbList": crumbs,
            "currentPage": page,
            "totalPage": totol_page,
            "websiteList": websites
        }

        return res


class CreatePage(Resource):
    """
    这里是创建一个模板的主页的资源类，模板的详情不在此，此类get只提供指定站点下的模板，以供选择
    """
    def get(self):
        website_id = request.args.get('website_id')
        if not website_id:
            return ERROR_RET_NO_PARAS
        website = query_single_website(website_id)
        if not website:
            return ERROR_RET_INVALID_PARAS
        category = query_single_category(website.category_id)

        crumbs = [
            {
                "title": "首页",
                "linkUrl": URL_PRIFIX + "/home"
            },
            {
                "title": category.name,
                "linkUrl": URL_PRIFIX + "/category?category_id={}".format(website.category_id)
            },
            {
                "title": website.name,
                "linkUrl": URL_PRIFIX + "/create?website_id={}".format(website.id)
            }
        ]

        templates = list()
        rows = query_website_template(website_id)
        for row in rows:
            templates.append(
                {
                    "templateName": row.name,
                    "templateId": row.id
                }
            )

        res = {
            'crumbList': crumbs,
            'templatetList': templates
        }

        return res


class TemplateDetailPage(Resource):
    """
    模板详细页面请求，描述模板的各部分信息
    """
    def get(self):
        template_id = request.args.get('template_id')
        if not template_id:
            return ERROR_RET_NO_PARAS

        template_des = query_template_description(template_id)
        if not template_des:
            return ERROR_RET_INVALID_PARAS

        """ 首先获取的【模板介绍】的信息 """
        template_description = {
            "tabName": "模板介绍",
            "contentType": "string",
            "description": template_des.description
        }

        """ 获取【字段预览】的信息 """
        filed_subtabs = list()
        filed_cn_headers = list()
        filed_headers = list()
        rows = query_template_fileds(template_id)
        for row in rows:
            filed_info = dict()
            filed_info['subTabName'] = row.filed_cn_name
            filed_cn_headers.append(row.filed_cn_name)
            filed_headers.append(row.filed_name)
            filed_info['contentType'] = row.filed_preview_type
            if filed_info['contentType'] == 'string':
                filed_info['description'] = row.filed_string
            elif filed_info['contentType'] == 'image':
                filed_info['image'] = row.filed_image

            filed_subtabs.append(filed_info)

        template_fileds = {
            "tabName": "字段预览",
            "contentType": "tabs",
            "subTabs": filed_subtabs
        }

        """ 获取【参数预览】信息 """
        para_cn_headers = list()
        para_headers = list()
        para_subtabs = list()
        rows = query_template_paras(template_id)
        for row in rows:
            para_info = dict()
            para_info['subTabName'] = row.para_cn_name
            para_info['contentType'] = row.para_preview_type
            if para_info['contentType'] == 'string':
                para_info['description'] = row.para_string
                para_cn_headers.append(row.para_cn_name)
                para_headers.append(row.para_name)
            elif para_info['contentType'] == 'image':
                para_info['image'] = row.para_image
                para_cn_headers.append(row.para_cn_name)
                para_headers.append(row.para_name)
            elif para_info['contentType'] == 'table':
                table_name = row.para_table
                example_rows = query_example(table_name, para_headers)
                para_info['headers'] = para_cn_headers
                para_info['data'] = [list(example_row) for example_row in example_rows]

            para_subtabs.append(para_info)

        template_paras = {
            "tabName": "采集参数预览",
            "contentType": "tabs",
            "subTabs": para_subtabs
        }

        """ 采集参数预览 """
        table_name = query_template_example(template_id).example_table
        example_rows = query_example(table_name, filed_headers)
        template_examples = {
            "tabName": "数据样例",
            "contentType": "table",
            "headers": filed_cn_headers,
            "data": [list(example_row) for example_row in example_rows]
        }

        res = {
            "tabs": [template_description, template_fileds, template_paras, template_examples]
        }

        return res


class TaskConfigPage(Resource):
    """
    任务配置页面
    """
    def get(self):
        template_id = request.args.get('template_id')
        if not template_id:
            return ERROR_RET_NO_PARAS
        single_template = query_single_template(template_id)
        if not single_template:
            return ERROR_RET_INVALID_PARAS
        res = {
            "templateName": single_template.name,
            "postFileLink": URL_PRIFIX + "/create/post_file",
            "previewLink": URL_PRIFIX + "/create/preview_file",
            "paraExampleLink": URL_PRIFIX + "/create/preview_example",
            "paraDownloadLink": URL_PRIFIX + "/create/download_example",
            "taskTypes": [
                {
                    "typeName": "定时任务",
                    "typeValue": TASK_TIMING_TYPE_CYCLE
                },
                {
                    "typeName": "一次性任务",
                    "typeValue": TASK_TIMING_TYPE_SINGLE,
                }
            ]
        }

        return res


class TaskCreateTaskPage(Resource):
    """
    任务创建流程，任务相关信息通过post传过来，在此处检查参数无误后，创建任务
    """
    @staticmethod
    def __check_paras(post_data):
        data_items = ['templateId', 'taskName', 'paraFileId', 'taskType', 'period']
        for item in data_items:
            if item not in post_data.keys():
                return False

            if post_data[item] is None:
                return False

        if post_data['taskType'] == TASK_TIMING_TYPE_CYCLE and not post_data['period']:
            return False

        return True

    def post(self):
        post_data = json.loads(request.get_data(as_text=True))

        if not self.__check_paras(post_data):
            return ERROR_RET_ERROR_PARAS

        file_id = post_data['paraFileId']
        if not query_para_file(file_id):
            return ERROR_RET_ERROR_FILE_ID

        return create_task(post_data)


class UploadParaFile(Resource):
    """
    上传参数文件，检查文件格式并将文件保存，返回生成文件的ID
    """
    @staticmethod
    def allowed_file(filename):  # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def post(self):
        file = request.files['file']
        if file and self.allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true
            uuid_str = str(uuid1())
            file_name = uuid_str + '.csv'
            file.save(os.path.join(UPLOAD_FOLDER, file_name))   # 保存文件
        else:
            return ERROR_RET_FILE_FORMAT_ERROR

        new_file = ParaFiles(id=uuid_str, file_name=file_name, create_time=datetime.now())
        db.session.add(new_file)
        db.session.commit()

        SUCCESS_RET_UPLOAD_SUCCESS['file_id'] = uuid_str

        return SUCCESS_RET_UPLOAD_SUCCESS


class PreviewFile(Resource):
    """
    参数文件预览，打开参数文件将数据预览
    """
    def get(self):
        file_id = request.args.get('file_id')
        if not file_id:
            return ERROR_RET_NO_PARAS
        file = query_para_file(file_id)
        if not file:
            return ERROR_RET_INVALID_PARAS
        file_name = UPLOAD_FOLDER + "\\" + query_para_file(file_id).file_name
        data = list()
        try:
            with open(file_name) as csv_file:
                reader = csv.reader(csv_file)
                for index, row in enumerate(reader):
                    if index == 0:
                        headers = row
                    else:
                        data.append(row)
        except Exception as e:
            log.error("处理预览文件失败 error：{}".format(str(e)))
            return ERROR_RET_PRO_PREVIEW_FILE

        res = {
            "headers": headers,
            "data": data
        }

        return res


class DownloadExample(Resource):
    """
    下载参数样例文件
    """
    def get(self):
        template_id = request.args.get('template_id')
        if not template_id:
            return ERROR_RET_NO_PARAS
        cur_template = query_single_template(template_id)
        if not cur_template:
            return ERROR_RET_INVALID_PARAS
        para_file = cur_template.para_file
        return send_from_directory(UPLOAD_FOLDER, filename=para_file, as_attachment=True)


class PreviewExample(Resource):
    """
    预览参数样例文件
    """
    def get(self):
        template_id = request.args.get('template_id')
        if not template_id:
            return ERROR_RET_NO_PARAS
        cur_template = query_single_template(template_id)
        if not cur_template:
            return  ERROR_RET_INVALID_PARAS
        para_file = UPLOAD_FOLDER + '\\' + cur_template.para_file
        data = list()
        with open(para_file) as csv_file:
            reader = csv.reader(csv_file)
            for index, row in enumerate(reader):
                if index == 0:
                    headers = row
                else:
                    data.append(row)
        res = {
            "headers": headers,
            "data": data
        }

        return res


class TasksPage(Resource):
    def get(self):
        tasks = query_tasks()
        headers = ['任务Id', '任务名称', '任务类型', '是否定时任务', '发布时间', '发布者', '运行状态', '任务控制',
                   '任务详情']
        task_list = list()
        for task in tasks:
            task_type = query_single_template(task.template_id).name
            if task.is_timing == 0:
                is_timing = "否"
            else:
                is_timing = "是"

            status = TASK_STATUS_DICT[task.status]

            task_list.append({
                "taskId": task.id,
                "taskName": task.name,
                "taskType": task_type,
                "isTiming": is_timing,
                "publishTime": str(task.publish_time),
                "user": "admin",
                "status": status,
                "taskControl": "/task/control",
                "taskDetail": "/task/detail?taskId={}".format(str(task.id))

            })

        res ={
            "taskHeaders": headers,
            "taskList": task_list
        }

        return res


class TaskControl(Resource):
    def get(self):
        task_id = request.args.get('task_id')
        operation = request.args.get('operation')
        if not task_id or not operation:
            return ERROR_RET_NO_PARAS
        cur_task = query_single_task(task_id)
        if not cur_task:
            return ERROR_RET_INVALID_PARAS
        cur_status = cur_task.status
        if operation == 'start':
            if cur_status in (TASK_STATUS_INIT, TASK_STATUS_FINISHED, TASK_STATUS_INTERRUPT):
                return start_task(task_id, cur_task.node_type)
            else:
                return ERROR_RET_TASK_STARTED

        if operation == 'stop':
            if cur_status == TASK_STATUS_RUNNING:
                return stop_task(cur_task)
            else:
                return ERROR_RET_NOT_START

        if operation == 'delete':
            return delete_task(cur_task)


class TaskDetailPage(Resource):
    def get(self):
        task_id = request.args.get('task_id')
        task_data = list()
        cur_task = query_single_task(task_id)
        if not cur_task:
            return {"res": "fail", "info": "指定任务不存在"}
        task_data.append({"rowName": "任务Id", "rowContent": cur_task.id})
        task_data.append({"rowName": "任务名称", "rowContent": cur_task.name})
        task_data.append({"rowName": "模板类型", "rowContent": query_single_template(cur_task.template_id).name})
        if cur_task.is_timing == 0:
            is_timing = "否"
        else:
            is_timing = "是"
        task_data.append({"rowName": "是否定时任务", "rowContent": is_timing})
        task_data.append({"rowName": "发布时间", "rowContent": str(cur_task.publish_time)})
        task_data.append({"rowName": "发布人", "rowContent": "admin"})
        status = TASK_STATUS_DICT[cur_task.status]
        task_data.append({"rowName": "运行状态", "rowContent": status})
        task_data.append({"rowName": "启动时间", "rowContent": str(cur_task.start_time)})
        task_data.append({"rowName": "完成时间", "rowContent": str(cur_task.end_time)})

        res = {
            "task_info": task_data,
            "task_control": URL_PRIFIX + "/task/control",
        }

        if cur_task.status == TASK_STATUS_FINISHED:
            export_data = {
                "type": ['csv'],
                'exportLink': URL_PRIFIX + "/task/download?task_id={}".format(task_id)
            }

            res['exportData'] = export_data

            filed_cn_headers = list()
            filed_headers = list()
            template_id = cur_task.template_id
            fields = query_template_fileds(template_id)
            res_table = cur_task.res_table
            for filed in fields:
                filed_cn_headers.append(filed.filed_cn_name)
                filed_headers.append(filed.filed_name)

            data = query_example(res_table, filed_headers)
            res['previewData'] = {
                "headers": filed_cn_headers,
                "data": [list(row) for row in data]
            }

        return res


class DownloadData(Resource):
    def get(self):
        task_id = request.args.get('task_id')
        cur_task = query_single_task(task_id)
        res_file = cur_task.res_file
        return send_from_directory(UPLOAD_FOLDER, filename=res_file, as_attachment=True)


class GlobalPage(Resource):
    def get(self):
        node_state = [
            {
                "title": "采集服务器数量",
                "type": "string",
                "value": query_nodes_count()
            },
            {
                "title": "采集服务器数量",
                "type": "string",
                "value": query_running_node_count()
            },
            {
                "title": "查看详情",
                "type": "link",
                "value": "查看详情",
                "link": URL_PRIFIX + "/golbal/nodes"
            }
        ]

        task_state = [
            {
                "title": "任务总数",
                "type": "string",
                "value": query_task_count()
            },
            {
                "title": "运行中任务数",
                "type": "string",
                "value": query_task_count(**{"status": 1}),
            },
            {
                "title": "已完成任务数",
                "type": "string",
                "value": query_task_count(**{"status": 3}),
            },
            {
                "title": "定时任务数",
                "type": "string",
                "value": query_task_count(**{"is_timing": 1}),
            },
        ]

        res = {
            "nodeState": node_state,
            "taskState": task_state
        }

        return res


class NodesPage(Resource):
    def get(self):
        nodes = query_nodes()
        headers = ["编号", "主机名称", "IP",  "服务器类型", "最大任务数", "运行任务数", "服务器状态"]
        data_list = list()
        for node in nodes:
            data_list.append([node.id, node.host_name, node.ip_addr, node.node_type, node.max_ps, node.cur_ps, node.status])
        res ={
            "headers": headers,
            "data": data_list
        }

        return res


class ImageDownload(Resource):
    def get(self, type):
        if type == 'website_logo':
            para_id = request.args.get('website_id')
            if not para_id:
                return ERROR_RET_INVALID_PARAS
            fold_name = IMAGE_FOLDER + "/" + type + "/"
            file_name = str(para_id) + '.png'
        elif type in ['para', 'field']:
            para_id = request.args.get('template_id')
            field_name = request.args.get('name')
            if not para_id or not field_name:
                return ERROR_RET_INVALID_PARAS
            fold_name = IMAGE_FOLDER + "\\" + type + "\\" + para_id
            file_name = field_name + '.png'
        else:
            return ERROR_RET_TYPE_ERROR

        return send_from_directory(fold_name, filename=file_name, as_attachment=True)


class TaskCsvExport(Resource):
    def get(self):
        task_id = request.args.get('task_id')
        cur_task = query_single_task(task_id)
        if not cur_task:
            return ERROR_RET_INVALID_PARAS

        template_id = cur_task.template_id
        table_name = cur_task.res_table
        cn_headers = list()
        fields = list()
        rows = query_template_fileds(template_id)
        for row in rows:
            cn_headers.append(row.filed_cn_name)
            fields.append(row.filed_name)

        rows = query_res_by_fields(table_name, fields)
        file_name = str(uuid1()) + '.csv'
        file_abs_name = UPLOAD_FOLDER + "\\" + file_name
        print(file_abs_name)
        with open(file_abs_name,  mode="w", newline='') as csv_file:
            out_csv = csv.writer(csv_file)
            out_csv.writerow(cn_headers)
            for row in rows:
                try:
                    out_csv.writerow(list(row))
                except:
                    print(row)

        update_task(task_id, 'res_file', file_name)

        return SUCCESS_RET_OPERATE_SUCCESS


class DebugTask(Resource):
    def get(self):
        task_id = request.args.get('task_id')
        opt = request.args.get('opt')
        if opt == 'stop':
            update_task(task_id, 'status', TASK_STATUS_INTERRUPT)


class DropNode(Resource):
    def get(self):
        node_id = request.args.get('node_id')
        db_delete_node(node_id)
        update_node_task(node_id, 'status', TASK_STATUS_INTERRUPT)
        return SUCCESS_RET_DEL_NODE




