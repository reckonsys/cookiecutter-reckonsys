from celery import Task
from celery.decorators import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class BaseTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: Emails in production
        # TODO: Validation
        logger.error('BaseTask ERROR', exc, task_id, args, kwargs, einfo)


task = task(base=BaseTask)  # noqa: F821
