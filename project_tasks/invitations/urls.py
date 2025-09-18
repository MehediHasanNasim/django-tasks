from django.urls import path
from .views import CreateInvitationView, accept_invitation, cancel_invitation

urlpatterns = [
    path('create/', CreateInvitationView.as_view(), name='create-invitation'),
    path('accept/', accept_invitation, name='accept-invitation'),
    path('cancel/<int:invitation_id>/', cancel_invitation, name='cancel-invitation'),
]