from celery import Celery

from node.config.celery_config import broker_url
from node.config.celery_config import result_backend
from node.config.celery_config import task_list
from node.config.celery_config import beat_schedule

"""
    celery -A app worker --loglevel=info
"""


def make_celery(app):
    celery = Celery("celery_server",
                    broker=broker_url,
                    backend=result_backend,
                    include=task_list)
    celery.config_from_object('node.config.celery_config')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
