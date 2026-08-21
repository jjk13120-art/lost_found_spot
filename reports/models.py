# reports/models.py

from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Documents', 'Documents'),
    ('Accessories', 'Accessories'),
    ('Others', 'Others'),
]

STATUS_CHOICES = [
    ('Lost', 'Lost'),
    ('Found', 'Found'),
    ('Solved', 'Solved'),
]

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='report_images/', null=True, blank=True)
    contact = models.CharField(max_length=100, help_text="Email or phone number")  # ✅ NEW FIELD
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} - {self.title}"

    def google_maps_url(self):
        return f"https://www.google.com/maps/search/?api=1&query={self.location.replace(' ', '+')}"