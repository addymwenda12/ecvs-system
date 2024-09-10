from django.db import models
from django.contrib.auth.models import AbstractUser
from blockchain.ethereum_utils import verify_credential
from blockchain.ipfs_utils import add_to_ipfs, get_from_ipfs
import json

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
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    date_issued = models.DateField()
    credential_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    is_verified = models.BooleanField(default=False)
    ipfs_hash = models.CharField(max_length=100, blank=True)
    private_data = models.JSONField(default=dict, blank=True)
    public_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        """
        Return a string representation of the credential.
        """
        return f"{self.degree} from {self.institution} ({self.date_issued})"

    def save(self, *args, **kwargs):
        if not self.ipfs_hash:
            credential_data = {
                'public': self.public_data,
                'private': self.private_data,
                'degree': self.degree,
                'institution': self.institution,
                'date_issued': str(self.date_issued),
                'credential_id': self.credential_id,
            }
            self.ipfs_hash = add_to_ipfs(json.dumps(credential_data))
        super().save(*args, **kwargs)

    def verify(self):
        is_verified, ipfs_hash = verify_credential(self.credential_id)
        self.is_verified = is_verified
        if is_verified and ipfs_hash:
            ipfs_data = get_from_ipfs(ipfs_hash)
            # Verify IPFS data matches the stored data
            if (ipfs_data['degree'] == self.degree and
                ipfs_data['institution'] == self.institution and
                ipfs_data['date_issued'] == str(self.date_issued) and
                ipfs_data['credential_id'] == self.credential_id):
                self.is_verified = True
            else:
                self.is_verified = False
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
