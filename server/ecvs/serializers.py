from rest_framework import serializers
from .models import Credential, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class CredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for credential model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Credential
        fields = ['id', 'degree', 'institution', 'date_issued', 'credential_id', 'created_at', 'user', 'user_id', 'is_verified']
        read_only_fields = ['id', 'created_at', 'is_verified']

    def create(self, validated_data):
        return Credential.objects.create(**validated_data)