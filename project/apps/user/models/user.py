from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    
    export_annotations = []
    export_fields = ["id", "username", "email", "is_active", "is_blocked"]
    
    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])
        
    def __str__(self) -> str:
        return f"{self.username} - {self.email}"