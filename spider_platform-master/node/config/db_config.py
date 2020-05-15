main_node_host = "http://192.168.108.80:5000"
main_node_host_dev = "http://192.168.6.242:5000"
main_node_host_test = "http://127.0.0.1:5000"

redis_host = "192.168.6.242"
redis_port = 6379
redis_max_connection = 100
redis_db = 0

redis_host_prod = "192.168.108.80"
redis_port_prod = 6379
redis_max_connection_prod = 100
redis_db_prod = 0

redis_host_dev = "192.168.6.242"
redis_port_dev = 6379
redis_max_connection_dev = 100
redis_db_dev = 0

redis_host_test = "localhost"
redis_port_test = 6379
redis_max_connection_test = 100
redis_db_test = 2

mysql_host = "192.168.108.80"
mysql_user = "root"
mysql_password = "root"
mysql_port = 3306
mysql_db = "spider_platform"
mysql_char = "utf8mb4"

mysql_host_dev = "192.168.6.242"
mysql_user_dev = "root"
mysql_password_dev = "root"
mysql_port_dev = 3306
mysql_db_dev = "spider_platform"
mysql_char_dev = "utf8mb4"

mysql_host_test = "localhost"
mysql_user_test = "admin"
mysql_password_test = "1q2w3e4r"
mysql_port_test = 3306
mysql_db_test = "node_test"
mysql_char_test = "utf8mb4"

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset={char}"

DATABASE_URL = DB_URI.format(username=mysql_user,
                             password=mysql_password,
                             host=mysql_host,
                             port=mysql_port,
                             db=mysql_db,
                             char=mysql_char)

DEV_DATABASE_URL = DB_URI.format(username=mysql_user_dev,
                                 password=mysql_password_dev,
                                 host=mysql_host_dev,
                                 port=mysql_port_dev,
                                 db=mysql_db_dev,
                                 char=mysql_char_dev)

TEST_DATABASE_URL = DB_URI.format(username=mysql_user_test,
                                  password=mysql_password_test,
                                  host=mysql_host_test,
                                  port=mysql_port_test,
                                  db=mysql_db_test,
                                  char=mysql_char_test)

TEST2_DATABASE_URL = None
