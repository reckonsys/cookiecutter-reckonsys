import eventlet
from django.conf import settings
from django.core.management.base import BaseCommand
from socketio import WSGIApp

from backend.contrib.events import sio


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        eventlet.monkey_patch()
        app = WSGIApp(sio)
        eventlet.wsgi.server(
            eventlet.listen(('', settings.SIO_SERVER_PORT)), app)
