from celery.schedules import crontab
from datetime import timedelta

# broker_url = 'amqp://localhost'
broker_url = 'redis://localhost/1'
result_backend = 'redis://localhost/6'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
# timezone = 'Europe/Oslo'
enable_utc = True

task_list = ['node.celery_task.task_read_redis',
             'node.celery_task.task_start_and_maintain']

# 需要执行任务的配置
beat_schedule = {
    'read_the_redis': {
        # 具体需要执行的函数
        # 该函数必须要使用@app.task装饰
        'task': 'node.celery_task.task_read_redis.start_task',
        # 定时时间
        # 每分钟执行一次，不能为小数
        'schedule': timedelta(seconds=10),
        'args': ()
    },
    'monitor_the_task': {
        # 具体需要执行的函数
        # 该函数必须要使用@app.task装饰
        'task': 'node.celery_task.task_start_and_maintain.task_monitor',
        # 定时时间
        # 每分钟执行一次，不能为小数
        'schedule': timedelta(seconds=30),
        'args': ()
    }
}
