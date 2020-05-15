import os
import redis

from flask_sqlalchemy import SQLAlchemy
from node.config import db_config
from common.log import log

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def redis_deploy():
    """Run production tasks."""
    # get the redis config with run type.
    run_type = os.getenv('FLASK_CONFIG') or 'default'
    print(f"Deploy redis config as run type: {run_type}")
    log.info(f"Deploy redis config as run type: {run_type}")
    if run_type == 'production':
        db_config.redis_db = db_config.redis_db_prod
        db_config.redis_host = db_config.redis_host_prod
        db_config.redis_max_connection = db_config.redis_max_connection_prod
        db_config.redis_port = db_config.redis_port_prod
    elif run_type == 'testing':
        db_config.redis_db = db_config.redis_db_test
        db_config.redis_host = db_config.redis_host_test
        db_config.redis_max_connection = db_config.redis_max_connection_test
        db_config.redis_port = db_config.redis_port_test
    else:
        db_config.redis_db = db_config.redis_db_dev
        db_config.redis_host = db_config.redis_host_dev
        db_config.redis_max_connection = db_config.redis_max_connection_dev
        db_config.redis_port = db_config.redis_port_dev


def generate_redis_pool():
    # Deploy the redis config
    redis_deploy()
    # 连接池连接使用，节省了每次连接用的时间
    print(f"Init redis pool to server in {db_config.redis_host}")
    log.info(f"Init redis pool to server in {db_config.redis_host}")
    pool = redis.ConnectionPool(host=db_config.redis_host, port=db_config.redis_port,
                                db=db_config.redis_db, max_connections=db_config.redis_max_connection)

    return pool


redis_pool = generate_redis_pool()

db = SQLAlchemy()
# db = SQLAlchemy(session_options={'autocommit': True})
