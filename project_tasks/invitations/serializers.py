from rest_framework import serializers
from .models import Invitation

class InvitationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['name', 'email', 'tenant', 'ip_address', 'note'] 
        read_only_fields = ['status', 'token', 'expiration_date']

class InvitationAcceptSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True) 

    def validate_token(self, value):
        try:
            invitation = Invitation.objects.get(token=value)
            if invitation.status != 'pending':
                raise serializers.ValidationError("Invitation is not valid.")
            if invitation.is_expired():
                invitation.status = 'expired'
                invitation.save()
                raise serializers.ValidationError("Invitation has expired.")
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        return value

class InvitationCancelSerializer(serializers.Serializer):
    pass