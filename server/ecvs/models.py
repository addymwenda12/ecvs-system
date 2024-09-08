from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        """
        Return a string representation of the credential.
        """
        return f"{self.degree} from {self.institution} ({self.date_issued})"

    def verify(self):
        # Simulate verification logic
        # Querying blockchain
        if self.credential_id.startswith("123"):
            return True
        else:
            return False
