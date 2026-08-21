from django.urls import path
from .views import scraped_items

urlpatterns = [
    path("scraped/",scraped_items, name="scraped_items"),
]
