# accounts/models.py
import os
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image and this.image:
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Profile.DoesNotExist:
            pass  # On first save, no file to delete

        super().save(*args, **kwargs)
