from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
     path('profile/update/', views.update_profile, name='update_profile'),
     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
