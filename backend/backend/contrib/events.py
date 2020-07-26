from celery import current_app

from backend.contrib.socket import sio

task = current_app.send_task
TASKS = 'backend.contrib.tasks.'


@sio.event
def connect(sid, data):
    task(f'{TASKS}connect', (sid, data))


@sio.event
def my_event(sid, data):
    task(f'{TASKS}my_event', (sid, data))


@sio.event
def disconnect(sid):
    task(f'{TASKS}disconnect', (sid, ))
