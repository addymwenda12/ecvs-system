from rest_framework import serializers
from .models import Credential, User

class CredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for the Credential model.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Credential
        fields = '__all__'

    def validate_user(self, value):
        if not value:
            raise serializers.ValidationError("User is required.")
        return value