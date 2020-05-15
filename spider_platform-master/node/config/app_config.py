import os
from common.log import log
from node.config import db_config

from node.core.global_parameter import node_running_info

basedir = os.path.abspath(os.path.dirname(__file__))

sqlite_dir = os.path.join(basedir, "instance")
try:
    if not os.path.exists(sqlite_dir):
        os.makedirs(sqlite_dir)
except Exception as e:
    print("Error in create path: {}".format(e))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = True

    JOBS = [
        {
            'id': 'get_task',
            'func': 'node:scheduler.start_read',
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'update_status',
            'func': 'node:scheduler.update_current_task_status',
            'trigger': 'interval',
            'seconds': 15
        },
        {
            'id': 'upload_node_info',
            'func': 'node:scheduler.upload_node_information',
            'trigger': 'date'
        }
    ]

    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_config.DEV_DATABASE_URL or \
                              'sqlite:///' + os.path.join(sqlite_dir, 'data-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        log.info("Config flask app as type development.")
        print("Config flask app as type development.")
        log.info(cls.SQLALCHEMY_DATABASE_URI)
        node_running_info.update({"main_node_host": db_config.mysql_host_dev})
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_config.TEST_DATABASE_URL or \
                              'sqlite:///' + os.path.join(sqlite_dir, 'data-test.sqlite')

    @classmethod
    def init_app(cls, app):
        log.info("Config flask app as type testing.")
        print("Config flask app as type testing.")
        log.info(cls.SQLALCHEMY_DATABASE_URI)
        node_running_info.update({"main_node_host": db_config.mysql_host_test})
        Config.init_app(app)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = db_config.DATABASE_URL or \
                              'sqlite:///' + os.path.join(sqlite_dir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        log.info("Config flask app as type production.")
        print("Config flask app as type production.")
        log.info(cls.SQLALCHEMY_DATABASE_URI)
        node_running_info.update({"main_node_host": db_config.mysql_host})
        Config.init_app(app)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
