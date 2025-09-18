# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.call_auth_service, name='auth_call'),
    path('billing/', views.call_billing_service, name='billing_call'),
]
