import logging
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth import authenticate, get_user_model
from .models import Credential, Wallet, User
from .serializers import CredentialSerializer, WalletSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from blockchain.ethereum_utils import issue_credential, verify_credential
import hashlib
import json
from blockchain.ipfs_utils import connect_to_ipfs

logger = logging.getLogger(__name__)

"""
ViewSets for the Credential model.
"""

class CredentialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Credential model.
    """
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new credential.
        """
        try:
            ipfs_client = connect_to_ipfs()
            if not ipfs_client:
                return Response({"error": "IPFS connection failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating credential: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Update a credential.
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return Response({"error": "A credential with this ID already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        credential = serializer.save()
        # Generate hash of the credential data
        hash_value = hashlib.sha256(f"{credential.degree}{credential.institution}{credential.date_issued}{credential.credential_id}".encode()).hexdigest()
        # Issue the credential on the blockchain
        issue_credential(credential.credential_id, hash_value, credential.ipfs_hash)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a credential.
        """
        try:
            credential = self.get_object()
            is_verified = verify_credential(credential.credential_id)
            return Response({'is_verified': is_verified})
        except Http404:
            return Response({"error": "Credential not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def selective(self, request, pk=None):
        credential = self.get_object()
        fields = request.query_params.get('fields', '').split(',')
        serializer = self.get_serializer(credential, context={'fields': fields})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def verifiable(self, request, pk=None):
        credential = self.get_object()
        return Response(json.loads(credential.to_verifiable_credential()))

    def destroy(self, request, *args, **kwargs):
        """
        Delete a credential
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting credential: {str(e)}")
            return Response({"error": "An error occurred while deleting the credential."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WalletView(APIView):
    """
    Viewset for Wallet model
    """
    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        if created:
            wallet.generate_address()
        wallet.update_balance()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def post(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        if created:
            wallet.generate_address()
        wallet.update_balance()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response(UserSerializer(user).data)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    User = get_user_model()
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            role=serializer.validated_data['role']
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)