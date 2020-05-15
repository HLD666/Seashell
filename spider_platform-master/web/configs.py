"""
Web接口及调度核心的配置信息
"""
import os

""" 数据库相关配置 """
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'spider_platform'
USERNAME = 'root'
PASSWORD = 'root'

DB_URI = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(username=USERNAME,
                                                                                        password=PASSWORD,
                                                                                        host=HOST, port=PORT,
                                                                                        db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 1024
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 600

""" 其他配置 """
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = BASE_DIR + r'/file'
IMAGE_FOLDER = BASE_DIR + r'/image'
ALLOWED_EXTENSIONS = ['csv']
SCAN_INTERVAL = 10
URL_PRIFIX = "/cmcc/data/spider"

