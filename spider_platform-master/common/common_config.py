""" 此文件定义调度核心和执行节点之间共同需要的全局变量 """

# Redis任务队列
REDIS_WINDOWS_TASKS = 'win_task_queue'
REDIS_LINUX_TASKS = 'lx_task_queue'

# 调度核心与执行节点交互
TASK_STOP_URL = "/task/control?task_id={task_id}&operation=stop"  # 通过此节点想执行代理发布控制
NODE_DROP_URL = "/drop_node?node_id={node_id}"
EXPORT_FILE_URL = "/export_file?task_id={task_id}"
QUERY_NODE_STATUS_URL = "/query_node"  # 查询指定执行节点状态

# 任务状态
TASK_STATUS_INIT = 0
TASK_STATUS_RUNNING = 1
TASK_STATUS_FINISHED = 2
TASK_STATUS_PREPARING = 3
TASK_STATUS_INTERRUPT = 5

# 任务运行类型
TASK_RUN_TYPE_WINDOWS = 0
TASK_RUN_TYPE_LINUX = 1

# 任务定时类型
TASK_TIMING_TYPE_SINGLE = 1
TASK_TIMING_TYPE_CYCLE = 2

# 节点状态
NODE_STATUS_NORMAL = 1
NODE_STATUS_DISCONNECT = 2
NODE_STATUS_INVALID = 3

# 任务脚本类型
TASK_EMBEDDED_SCRIPT = 0
TASK_EXTERNAL_SCRIPT = 1

HOT_WEBSITE_COUNT = 12


ERROR_RET_NO_PARAS = {"ret": 'fail', 'info': '缺少必要参数'}
ERROR_RET_INVALID_PARAS = {"ret": 'fail', 'info': '参数无效'}
ERROR_RET_ERROR_PARAS = {"ret": 'fail', 'info': '参数错误'}
ERROR_RET_ERROR_FILE_ID = {"ret": 'fail', 'info': '参数文件无效'}
ERROR_RET_UPLOAD_FILE_ERROR = {"ret": 'fail', 'info': '上传文件格式错误'}
ERROR_RET_UNKNOWN_TASK_TYPE = {"ret": "fail", "info": "未知任务类型"}
ERROR_RET_CANNOT_CONNECT_NODE = {"ret": "fail", "info": "执行节点通信失败"}
ERROR_RET_FILE_FORMAT_ERROR = {"ret": "fail", "info": "文件格式错误"}
ERROR_RET_PRO_PREVIEW_FILE = {"ret": "fail", "info": "打开预览文件失败"}
ERROR_RET_TASK_STARTED = {"ret": "fail", "info": "任务已经启动"}
ERROR_RET_NOT_START = {"ret": "fail", "info": "任务未启动"}
ERROR_RET_TYPE_ERROR = {"ret": "fail", "info": "类型错误"}
ERROR_RET_DELETE_TASK = {"ret": "fail", "info": "任务删除失败"}
ERROR_RET_STOP_TASK = {"ret": "fail", "info": "任务停止失败"}


SUCCESS_RET_CREATE_TASK = {"ret": 'success', 'info': '任务创建成功'}
SUCCESS_RET_START_TASK = {"ret": "success", "info": "任务启动成功"}
SUCCESS_RET_STOP_TASK = {"ret": "success", "info": "任务停止成功"}
SUCCESS_RET_DELETE_TASK = {"ret": "success", "info": "任务删除成功"}
SUCCESS_RET_OPERATE_SUCCESS = {"ret": "success", "info": "操作成功"}
SUCCESS_RET_UPLOAD_SUCCESS = {"ret": "success", "info": "文件上传成功"}
SUCCESS_RET_DEL_NODE = {"ret": "success", "info": "节点删除成功"}

TASK_STATUS_DICT = {
    TASK_STATUS_INIT: "未开始",
    TASK_STATUS_RUNNING: "运行中",
    TASK_STATUS_FINISHED: "已完成",
    TASK_STATUS_PREPARING: "调度中",
    TASK_STATUS_INTERRUPT: "任务终止"
}


