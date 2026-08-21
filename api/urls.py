from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_data_api, name='api-reports'),
    path('user-count/', views.user_count_api, name='api-user-count'),
]
