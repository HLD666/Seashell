"""----------------------------------------插件扩展-------------------------------------------------------------------"""

from flask_sqlalchemy import SQLAlchemy
import redis

# 连接池连接使用，节省了每次连接用的时间
redis_pool = redis.ConnectionPool(host='localhost', port=6379, max_connections=100)

db = SQLAlchemy(session_options={'autocommit': True})
