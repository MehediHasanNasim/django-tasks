import requests
from django.conf import settings
from functools import wraps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Feature, Role, RoleFeaturePermission


def check_permission(product_id, feature, permission):
    """
    Decorator to check if the user's role has the required permission on a product-feature.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)

            tenant = user.tenant  
            user_role = user.role  

            if not user_role:
                return JsonResponse({"error": "No role assigned"}, status=403)

            product = get_object_or_404(Product, id=product_id)
            feature_obj = get_object_or_404(Feature, product=product, name=feature)

            has_perm = RoleFeaturePermission.objects.filter(
                role=user_role,
                feature=feature_obj,
                permission=permission
            ).exists()

            if not has_perm:
                return JsonResponse(
                    {"error": f"Permission denied: {permission} on {feature} in product {product_id}"},
                    status=403
                )

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator