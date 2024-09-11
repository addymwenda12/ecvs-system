import logging
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from .models import Credential, Wallet, User
from .serializers import CredentialSerializer, WalletSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from blockchain.ethereum_utils import issue_credential, verify_credential, get_balance
import hashlib
import json
from rest_framework.authtoken.models import Token


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
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            logger.error(f"Validation error creating credential: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error creating credential: {str(e)}")
            return Response({"error": "An unexpected error occurred while creating the credential."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        credential = serializer.save(is_verified=False)  # Initially set as unverified
        # Generate hash of the credential data
        hash_value = hashlib.sha256(f"{credential.degree}{credential.institution}{credential.date_issued}{credential.credential_id}".encode()).hexdigest()
        # Issue the credential on the blockchain
        try:
            tx_receipt = issue_credential(credential.credential_id, hash_value)
            if tx_receipt['status'] == 1:  # Transaction was successful
                credential.is_verified = True
                credential.save()
                logger.info(f"Credential {credential.credential_id} verified on blockchain")
            else:
                logger.warning(f"Blockchain transaction failed for credential {credential.credential_id}")
        except Exception as e:
            logger.error(f"Error issuing credential: {str(e)}")
            # Log the error but don't raise an exception to allow credential creation
            logger.warning(f"Credential created but not verified on blockchain: {credential.credential_id}")
        return credential

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

    @action(detail=False, methods=['post'])
    def scan_verify(self, request):
        """
        Scan and verify a credential by ID or institution name.
        """
        identifier = request.data.get('identifier')
        if not identifier:
            return Response({"error": "Identifier is required"}, status=status.HTTP_400_BAD_REQUEST)

        credential, is_verified = Credential.verify_by_id_or_institution(identifier)
        if credential:
            serializer = self.get_serializer(credential)
            return Response({
                'credential': serializer.data,
                'is_verified': is_verified
            })
        else:
            return Response({"error": "Credential or institution not found"}, status=status.HTTP_404_NOT_FOUND)

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def balance(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        if created:
            wallet.generate_address()
        wallet.update_balance()
        return Response({'balance': wallet.balance})

    @action(detail=False, methods=['POST'])
    def generate(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        if created or not wallet.address:
            wallet.generate_address()
        wallet.update_balance()
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        logger.info(f"Login attempt for user: {request.data.get('username')}")
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            try:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'wallet': WalletSerializer(user.wallet).data if hasattr(user, 'wallet') else None
                })
            except Exception as e:
                logger.error(f"Error creating token: {str(e)}")
                return Response({"error": "An error occurred during login"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
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
        password = serializer.validated_data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=password,
            role=serializer.validated_data.get('role')
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)