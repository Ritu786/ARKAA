from celery import Celery

celery_app = Celery(
    'indexing_files',
    broker='amqp://guest:guest@localhost:5672//', #RabbitMQ Broker
    backend='rpc://'
)


'''
Defines which task should go which queue.
    - tasks.indexing_task.run_indexing = taks.module_name.function_name
    - that means run_indexing task will be routed to a queue named indexing_queue.
'''
celery_app.conf.task_routes = {
    "tasks.indexing_task.run_indexing": {"queue":"indexing_queue"},
}

import api.v1.tasks.indexing_task

# celery_app.autodiscover_tasks(["api.v1.tasks"])


