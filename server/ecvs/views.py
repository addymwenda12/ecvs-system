from rest_framework import viewsets
from .models import Credential
from .serializers import CredentialSerializer
"""
ViewSets for the Credential model.
"""
class CredentialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Credential model.
    """
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer