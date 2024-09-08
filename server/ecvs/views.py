import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
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
            logger.info(f"Creating credential: {request.data}")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List all credentials.
        """
        try:
            logger.info(f"Listing credentials")
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a credential by ID.
        """
        try:
            logger.info(f"Retrieving credential by ID: {kwargs['pk']}")
            return super().retrieve(request, *args, **kwargs)
        except Credential.DoesNotExist:
            return Response({"error": "Credential not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Update a credential by ID.
        """
        try:
            logger.info(f"Updating credential by ID: {kwargs['pk']}")
            return super().update(request, *args, **kwargs)
        except Credential.DoesNotExist:
            return Response({"error": "Credential not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a credential by ID.
        """
        try:
            logger.info(f"Deleting credential by ID: {kwargs['pk']}")
            return super().destroy(request, *args, **kwargs)
        except Credential.DoesNotExist:
            return Response({"error": "Credential not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)