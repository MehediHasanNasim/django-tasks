# auth-service/core/views.py
from django.http import JsonResponse
import logging
import requests
from .logging_conf import get_trace_id

logger = logging.getLogger(__name__)

def trigger_cross_service(request):
    """
    A simple endpoint: logs locally, calls tenant-service and forwards trace id.
    """
    trace_id = getattr(request, "trace_id", None)
    logger.info("auth-service: trigger received", extra={"note": "start trigger"})

    tenant_service_url = "http://<url>:8001/api/tenant/log/"
    headers = {}
    if trace_id:
        headers["X-Trace-ID"] = trace_id

    try:
        resp = requests.post(tenant_service_url, json={"msg": "hello from auth"}, headers=headers, timeout=5)
        logger.info("auth-service: called tenant-service", extra={"status_code": resp.status_code})
    except Exception as exc:
        logger.exception("auth-service: failed calling tenant-service")

    return JsonResponse({"ok": True, "trace_id": trace_id})
