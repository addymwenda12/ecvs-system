from rest_framework import serializers
from .models import Credential

class CredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for the Credential model.
    """
    class Meta:
        model = Credential
        fields = '__all__'