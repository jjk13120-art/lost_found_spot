from django.urls import path
from . import views

app_name = "feedback"

urlpatterns = [
    path("", views.submit_feedback, name="feedback"),
    path("share-story/", views.share_story, name="share_story"),
]
