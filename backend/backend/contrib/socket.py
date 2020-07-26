from socketio import RedisManager, Server

from django.conf import settings


mgr = RedisManager(settings.REDIS_URL)  # , write_only=True)

sio = Server(client_manager=mgr, cors_allowed_origins='*')


def _emit(event_name, sid, data):
    return sio.emit(event_name, data, to=sid)


def emit_error(sid, data):
    return _emit('error', sid, data)


def emit_my_event(sid, data):
    return _emit('my_event', sid, data)
