from rest_framework import serializers
from .models import Credential, User
from django.core.exceptions import ValidationError
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    wallet = WalletSerilizer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'wallet']

class CredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for credential model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    public_data = serializers.JSONField(required=False)
    private_data = serializers.JSONField(required=False, write_only=True)

    class Meta:
        model = Credential
        fields = ['id', 'degree', 'institution', 'date_issued', 'credential_id', 'created_at', 'user', 'user_id', 'is_verified', 'public_data', 'private_data']
        read_only_fields = ['id', 'created_at', 'is_verified']

    def validate_degree(self, value):
        """
        Validate the degree field.
        """
        if len(value) < 2:
            raise serializers.ValidationError("Degree must be at least 2 characters long.")
        return value

    def validate_institution(self, value):
        """
        Validate the institution field.
        """
        if len(value) < 2:
            raise serializers.ValidationError("Institution must be at least 2 characters long.")
        return value

    def validate_date_issued(self, value):
        """
        Validate the date issued field.
        """
        if value > timezone.now().date():
            raise serializers.ValidationError("Date issued cannot be in the future.")
        return value

    def validate_credential_id(self, value):
        """
        Validate credential ID
        """
        if Credential.objects.filter(credential_id=value).exists():
            raise serializers.ValidationError("This credential ID already exists.")
        return value

    def create(self, validated_data):
        """
        Create credentials
        """
        return Credential.objects.create(**validated_data)

    def to_representation(self, instance):
        user = self.context['request'].user if 'request' in self.context else None
        if user and user == instance.user:
            return instance.get_private_view()
        return instance.get_public_view()

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for wallet model
    """
    class Meta:
        model = Wallet
        fields = ['address', 'balance']
        read_only_fields = ['balance']