import logging
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from .models import Credential, Wallet
from .serializers import CredentialSerializer, WalletSerializer
from blockchain.ethereum_utils import issue_credential
import hashlib

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
            logger.error(f"Validation error: {str(e)}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return Response({"error": "A credential with this ID already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            is_verified = credential.verify()
            return Response({'is_verified': is_verified})
        except Http404:
            return Response({"error": "Credential not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def post(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        if created:
            # Here you would typically generate a new Ethereum address
            # For simplicity, we're just using a placeholder
            wallet.address = f"0x{request.user.id:040x}"
            wallet.save()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)