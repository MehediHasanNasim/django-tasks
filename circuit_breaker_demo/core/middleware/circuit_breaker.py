# core/middleware/circuit_breaker.py
import time
import logging
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class ExternalServiceCircuitBreakerMiddleware:
    """
    Circuit Breaker Middleware for outbound HTTP requests.
    Tracks failing domains and blocks them if failures exceed threshold.
    """

    FAILURE_THRESHOLD = 3           # Failures to trigger circuit
    FAILURE_WINDOW = 60             # Seconds
    BLOCK_TIME = 120                # Seconds blocked

    # Domains to monitor
    MONITORED_DOMAINS = ['auth-service.com', 'billing-service.com']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.call_external_service = self.call_external_service
        response = self.get_response(request)
        return response

    def call_external_service(self, domain, func, *args, **kwargs):
        """
        func should be a callable that makes the actual HTTP request.
        Example: func = lambda: requests.get(url)
        """
        if domain not in self.MONITORED_DOMAINS:
            return func(*args, **kwargs)

        circuit_key = f'circuit:{domain}'
        failure_key = f'failures:{domain}'

        circuit_state = cache.get(circuit_key)
        if circuit_state == 'OPEN':
            logger.warning(f"Blocked request to {domain} (circuit open).")
            return JsonResponse(
                {"error": f"{domain} is temporarily unavailable due to failures."},
                status=503
            )

        try:
            response = func(*args, **kwargs)

            if 500 <= getattr(response, 'status_code', 0) < 600:
                self.record_failure(domain)
            else:
                self.reset_failures(domain)
            return response

        except Exception as e:
            logger.exception(f"Error calling {domain}: {e}")
            self.record_failure(domain)
            return JsonResponse({"error": "External service call failed."}, status=503)

    def record_failure(self, domain):
        failure_key = f'failures:{domain}'
        circuit_key = f'circuit:{domain}'

        failures = cache.get(failure_key, [])
        now = time.time()
        failures = [t for t in failures if now - t < self.FAILURE_WINDOW]
        failures.append(now)
        cache.set(failure_key, failures, timeout=self.FAILURE_WINDOW)

        logger.warning(f"Failure recorded for {domain}. Total recent failures: {len(failures)}")

        if len(failures) >= self.FAILURE_THRESHOLD:
            cache.set(circuit_key, 'OPEN', timeout=self.BLOCK_TIME)
            logger.error(f"Circuit opened for {domain} for {self.BLOCK_TIME} seconds.")

    def reset_failures(self, domain):
        failure_key = f'failures:{domain}'
        cache.delete(failure_key)
        logger.info(f"Failures reset for {domain}.")
