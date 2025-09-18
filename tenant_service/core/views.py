from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def receive_log(request):
    logger.info("tenant-service: received cross-service call", extra={"payload": request.body.decode()})
    return JsonResponse({"ok": True})
