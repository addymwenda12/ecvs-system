from django.shortcuts import render, redirect
from .models import Credential
from .forms import CredentialForm
"""
Views for the ECVS application.
"""

def create_credential(request):
    """
    View to create a new credential.
    """
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('credential_list')
    else:
        form = CredentialForm()
    return render(request, 'create_credential.html', {'form': form})

def credential_list(request):
    """
    View to list all credentials.
    """
    credentials = Credential.objects.all()
    return render(request, 'credential_list.html', {'credentials': credentials})

def verify_credential(request, credential_id):
    """
    View to verify a credential by ID.
    """
    try:
        credential = Credential.objects.get(credential_id=credential_id)
        is_verified = credential.verify()
        return render(request, 'verify_credential.html', {'credential': credential, 'is_verified': is_verified})
    except Credential.DoesNotExist:
        return render(request, 'verify_credential.html', {'error': 'Credential not found'})
