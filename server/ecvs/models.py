from django.db import models
from django.contrib.auth.models import AbstractUser
from blockchain.ethereum_utils import verify_credential
from blockchain.ipfs_utils import add_to_ipfs, get_from_ipfs
import json
from cryptography.fernet import Fernet
from django.conf import settings

class User(AbstractUser):
    """
    Custom user model
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employer', 'Employer'),
        ('institution', 'Institution'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class Credential(models.Model):
    """
    A credential represents a degree or certificate issued by an institution.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    date_issued = models.DateField()
    credential_id = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)
    public_data = models.JSONField(default=dict, blank=True)
    private_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the credential.
        """
        return f"{self.degree} from {self.institution}"

    def verify(self):
        is_verified = verify_credential(self.credential_id)
        self.is_verified = is_verified
        self.save()
        return self.is_verified

    def get_public_view(self):
        return {
            'degree': self.degree,
            'institution': self.institution,
            'date_issued': self.date_issued,
            'is_verified': self.is_verified,
            **self.public_data
        }

    def get_private_view(self):
        return {
            'degree': self.degree,
            'institution': self.institution,
            'date_issued': self.date_issued,
            'is_verified': self.is_verified,
            'credential_id': self.credential_id,
            **self.public_data,
            **self.private_data
        }

    def get_selective_view(self, fields):
        allowed_fields = set(self.get_private_view().keys())
        requested_fields = set(fields)
        valid_fields = allowed_fields.intersection(requested_fields)
        return {field: getattr(self, field) for field in valid_fields}

    def to_verifiable_credential(self):
        from blockchain.verifiable_credential import VerifiableCredential
        return VerifiableCredential(self).to_json()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    address = models.CharField(max_length=42, unique=True)
    balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    encrypted_private_key = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return f"Wallet for {self.user.username}"

    def set_private_key(self, private_key):
        f = Fernet(settings.ENCRYPTION_KEY)
        self.encrypted_private_key = f.encrypt(private_key.encode())

    def get_private_key(self):
        if self.encrypted_private_key:
            f = Fernet(settings.ENCRYPTION_KEY)
            return f.decrypt(self.encrypted_private_key).decode()
        return None

    def generate_address(self):
        from blockchain.ethereum_utils import generate_ethereum_address
        address, private_key = generate_ethereum_address()
        self.address = address
        self.set_private_key(private_key)
        self.save()

    def update_balance(self):
        from blockchain.ethereum_utils import get_balance
        self.balance = get_balance(self.address)
        self.save()
