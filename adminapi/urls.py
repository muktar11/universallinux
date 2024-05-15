"""
URL configuration for adminapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# yourproject/urls.py
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Account/', include('Account.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # Route for serving media files
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Route for serving index.html
urlpatterns += [
    re_path(r'^', TemplateView.as_view(template_name='index.html')),
]

# Additional static URL
urlpatterns += [
    path('additional-url/', TemplateView.as_view(template_name='additional_template.html')),
]