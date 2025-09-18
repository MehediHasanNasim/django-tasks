from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import Invitation
from .serializers import InvitationCreateSerializer, InvitationAcceptSerializer, InvitationCancelSerializer
from django.db import IntegrityError


class CreateInvitationView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer

    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR')
        invitation = serializer.save(ip_address=ip_address)
        self.send_invitation_email(invitation)

    def send_invitation_email(self, invitation):
        print(f"Simulating email sent to {invitation.email} with token {invitation.token}")
    

@api_view(['POST'])
def accept_invitation(request):
    serializer = InvitationAcceptSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        try:
            invitation = Invitation.objects.get(token=token)
            user = create_user_from_invitation(invitation, password)
            invitation.status = 'accepted'
            invitation.save()
            return Response({"message": "Invitation accepted. User created."}, status=status.HTTP_200_OK)
        except Invitation.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_user_from_invitation(invitation, password):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.create_user(
            username=invitation.email,
            email=invitation.email,
            password=password,
            first_name=invitation.name,
            tenant=invitation.tenant  
        )
        return user
    except IntegrityError:
        raise ValueError("User already exists.")

@api_view(['POST'])
def cancel_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id)
        if invitation.status != 'pending':
            return Response({"error": "Only pending invitations can be canceled."}, status=status.HTTP_400_BAD_REQUEST)
        invitation.status = 'canceled'
        invitation.save()
        return Response({"message": "Invitation canceled."}, status=status.HTTP_200_OK)
    except Invitation.DoesNotExist:
        return Response({"error": "Invitation not found."}, status=status.HTTP_404_NOT_FOUND)