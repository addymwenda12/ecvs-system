from django.db import models

class Credential(models.Model):
    """
    A credential represents a degree or certificate issued by an institution.
    """
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    date_issued = models.DateField()
    credential_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the credential.
        """
        return f"{self.degree} from {self.institution} ({self.date_issued})"

    def verify(self):
        # Logic to verify the credential (e.g., check against a blockchain)
        return True  # Placeholder for actual verification logic

