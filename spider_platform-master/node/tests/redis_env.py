import redis
import node.config.db_config as db_config

# 连接池连接使用，节省了每次连接用的时间
redis_pool = redis.ConnectionPool(host=db_config.redis_host_test, port=db_config.redis_port_test,
                                  db=db_config.redis_db_test, max_connections=db_config.redis_max_connection_test)

redis_pool_dev = redis.ConnectionPool(host=db_config.redis_host, port=db_config.redis_port,
                                      db=db_config.redis_db, max_connections=db_config.redis_max_connection)

redis_pool_prod = redis.ConnectionPool(host=db_config.redis_host_prod, port=db_config.redis_port_prod,
                                       db=db_config.redis_db_prod, max_connections=db_config.redis_max_connection_prod)


def insert_test_list():
    redis_conn = redis.Redis(connection_pool=redis_pool)
    for test_id in range(60):
        redis_conn.lpush("win_task_queue", str((1, "start")))
        redis_conn.lpush("lx_task_queue", str((1, "start")))


def insert_dev_list():
    redis_conn = redis.Redis(connection_pool=redis_pool_dev)
    for test_id in range(1):
        redis_conn.lpush("win_task_queue", str((13, "start")))
        redis_conn.lpush("lx_task_queue", str((13, "start")))


def insert_prod_list():
    redis_conn = redis.Redis(connection_pool=redis_pool_prod)
    for test_id in range(1):
        redis_conn.lpush("win_task_queue", str((19, "start")))
        redis_conn.lpush("lx_task_queue", str((19, "start")))


if __name__ == "__main__":
    # insert_test_list()
    # insert_dev_list()
    insert_prod_list()
