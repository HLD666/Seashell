import os

from node.config import db_config
from common.log import log

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../node/.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_DATABASE = "data_res"


def database_config_deploy():
    # get the spider mysql config with run type.
    run_type = os.getenv('FLASK_CONFIG') or 'default'
    print(f"Deploy spider mysql config as run type: {run_type}")
    log.info(f"Deploy spider mysql config as run type: {run_type}")

    db_database = DB_DATABASE
    if run_type == 'production':
        db_host = db_config.mysql_host
        db_user = db_config.mysql_user
        db_password = db_config.mysql_password
        db_port = db_config.mysql_port
        db_char = db_config.mysql_char
    elif run_type == 'testing':
        db_host = db_config.mysql_host_test
        db_user = db_config.mysql_user_test
        db_password = db_config.mysql_password_test
        db_port = db_config.mysql_port_test
        db_char = db_config.mysql_char_test
    else:
        db_host = db_config.mysql_host_dev
        db_user = db_config.mysql_user_dev
        db_password = db_config.mysql_password_dev
        db_port = db_config.mysql_port_dev
        db_char = db_config.mysql_char_dev

    return db_config.DB_URI.format(username=db_user,
                                   password=db_password,
                                   host=db_host,
                                   port=db_port,
                                   db=db_database,
                                   char=db_char)


SPIDER_DB_URI = database_config_deploy()
