import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Credential
from .serializers import CredentialSerializer

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
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return Response({"error": "A credential with this ID already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a credential.
        """
        try:
            credential = self.get_object()
            is_verified = credential.verify()
            return Response({'is_verified': is_verified})
        except Exception as e:
            logger.error(f"Error verifying credential: {str(e)}")
            return Response({"error": "An error occurred while verifying the credential."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a credential
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting credential: {str(e)}")
            return Response({"error": "An error occurred while deleting the credential."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)