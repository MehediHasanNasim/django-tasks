import requests
from django.http import JsonResponse

def call_auth_service(request):
    url = 'https://auth-service.com/fail-endpoint'  # Simulate a failing endpoint

    def make_request():
        return requests.get(url, timeout=5)

    response = request.call_external_service('auth-service.com', make_request)
    return response

def call_billing_service(request):
    url = 'https://billing-service.com/fail-endpoint'  # Simulate a failing endpoint

    def make_request():
        return requests.get(url, timeout=5)

    response = request.call_external_service('billing-service.com', make_request)
    return response
