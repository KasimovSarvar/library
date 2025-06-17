from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from abstraction.base_models import BaseModel
from django.db import models

class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Student'),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        role = "Admin" if self.role == 0 else "Student"
        return f"{self.username} ({role})"
