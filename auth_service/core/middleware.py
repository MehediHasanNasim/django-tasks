import uuid
from django.utils.deprecation import MiddlewareMixin
from .logging_conf import set_trace_id, set_user_id, set_tenant_id

class TraceIdMiddleware(MiddlewareMixin):

    def process_request(self, request):
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
        set_trace_id(trace_id)

        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            set_user_id(getattr(user, "id", ""))
        else:
            set_user_id(None)
            set_tenant_id(None)

        request.trace_id = trace_id

    def process_response(self, request, response):
        trace_id = getattr(request, "trace_id", None)
        if trace_id:
            response["X-Trace-ID"] = trace_id
        return response
