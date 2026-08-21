"""
URL configuration for mylostfound project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('reports/', include('reports.urls', namespace='reports')),
   path('feedback/', include(('feedback.urls', 'feedback'), namespace='feedback')),
    path('scraping/', include('scraping.urls')),
    path('api/', include('api.urls')),
     path('features/', include('features.urls')),
    path('faq/', include('faq.urls')),
    path("terms/", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
]
urlpatterns += [
    path("dashboard/", TemplateView.as_view(template_name="pages/dashboard.html"), name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)