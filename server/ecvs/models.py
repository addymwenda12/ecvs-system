from django.db import models
from django.contrib.auth.models import AbstractUser
from blockchain.ethereum_utils import verify_credential

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

    def __str__(self):
        """
        Return a string representation of the credential.
        """
        return f"{self.degree} from {self.institution} ({self.date_issued})"

    def verify(self):
        # Use the blockchain to verify the credential
        self.is_verified = verify_credential(str(self.id))
        self.save()
        return self.is_verified
