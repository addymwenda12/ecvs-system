from django import forms
from .models import Credential

class CredentialForm(forms.ModelForm):
    """
    Form for creating a new credential.
    """
    class Meta:
        model = Credential
        fields = ['degree', 'institution', 'date_issued', 'credential_id']
