import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
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

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify the credential.
        """
        credential = self.get_object()
        is_verified = credential.verify()
        return Response({'is_verified': is_verified})

    def perform_create(self, serializer):
        """
        Perform the create action.
        """
        serializer.save()

    def list(self, request, *args, **kwargs):
        """
        List all credentials.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a credential.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a credential.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a credential.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)