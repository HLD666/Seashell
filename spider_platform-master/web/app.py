import sys
sys.path.append("..")
from flask import Flask, redirect, url_for
from flask_restful import Api
import configs
from resource import *
from exts import db
from timer import TaskTimer
from common import log
from configs import URL_PRIFIX


app = Flask(__name__)
app.config.from_object(configs)
db.init_app(app)
api = Api(app)

""" 主页、搜索页、品类页面 """
api.add_resource(HomePage, URL_PRIFIX + '/home')
api.add_resource(SearchPage, URL_PRIFIX + '/search')
api.add_resource(CategoryPgae, URL_PRIFIX + '/category')
""" 创建系列页面 """
api.add_resource(CreatePage, URL_PRIFIX + '/create')
api.add_resource(TemplateDetailPage, URL_PRIFIX + '/create/template_detail')
api.add_resource(TaskConfigPage, URL_PRIFIX + '/create/config')
api.add_resource(TaskCreateTaskPage, URL_PRIFIX + '/create/create_task')
api.add_resource(UploadParaFile, URL_PRIFIX + '/create/post_file')
api.add_resource(PreviewFile, URL_PRIFIX + '/create/preview_file')
api.add_resource(DownloadExample, URL_PRIFIX + '/create/download_example')
api.add_resource(PreviewExample, URL_PRIFIX + '/create/preview_example')
""" 任务查询，控制 """
api.add_resource(TasksPage, URL_PRIFIX + '/tasks')
api.add_resource(TaskControl, URL_PRIFIX + '/task/control')
api.add_resource(TaskDetailPage, URL_PRIFIX + '/task/detail')
api.add_resource(DownloadData, URL_PRIFIX + '/task/download')
""" 全局状态查询 """
api.add_resource(GlobalPage, URL_PRIFIX + '/global')
api.add_resource(NodesPage, URL_PRIFIX + '/global/nodes')
""" 图片获取 """
api.add_resource(ImageDownload, URL_PRIFIX + '/image/<type>')
""" 将数据转换为csv文件 """
api.add_resource(TaskCsvExport, '/export_file')

api.add_resource(DebugTask, '/debug_task')

api.add_resource(DropNode, '/drop_node')


@app.route('/')
def hello_world():
    return redirect(URL_PRIFIX + '/home')


if __name__ == '__main__':
    log.info("调度核心启动")
    task_timer = TaskTimer()
    task_timer.start()
    app.run(host="0.0.0.0", use_reloader=False, debug=True)
