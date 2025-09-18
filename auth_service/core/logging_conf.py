import logging
import contextvars
import os

_trace_id = contextvars.ContextVar("trace_id", default=None)
_user_id = contextvars.ContextVar("user_id", default=None)
_tenant_id = contextvars.ContextVar("tenant_id", default=None)

SERVICE_NAME = os.environ.get("SERVICE_NAME", "auth-service")

def set_trace_id(val):
    _trace_id.set(val)

def get_trace_id():
    return _trace_id.get()

def set_user_id(val):
    _user_id.set(val)

def get_user_id():
    return _user_id.get()

def set_tenant_id(val):
    _tenant_id.set(val)

def get_tenant_id():
    return _tenant_id.get()


class RequestContextFilter(logging.Filter):

    def filter(self, record):
        record.trace_id = get_trace_id() or ""
        record.service_name = SERVICE_NAME
        record.user_id = get_user_id() or ""
        record.tenant_id = get_tenant_id() or ""
        return True
