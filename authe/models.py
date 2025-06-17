from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Student'),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)

    def __str__(self):
        role = "Admin" if self.role == 0 else "Student"
        return f"{self.username} ({role})"
