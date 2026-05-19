from .servicies.MessageProcess import process
from celery import shared_task


@shared_task()
def process_message(external_message_id):
    return process(external_message_id)