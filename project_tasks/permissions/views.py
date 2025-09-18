from django.http import JsonResponse
from .decorators import check_permission

@check_permission(product_id="abc", feature="dashboard", permission="read")
def dashboard_view(request):
    return JsonResponse({"message": "You have access to the dashboard!"})