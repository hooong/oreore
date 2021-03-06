"""oreore_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
import index.views
import prescription_read.views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.views.index, name='index'),
    path('contact/', index.views.contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('prescription/', include('prescription_manage.urls')),
    path('disease/', include('disease_manage.urls')),
    path('prescription_read/', include('prescription_read.urls')),
    path('medicine/', include('medicine_manage.urls')),
    path('index/', include('index.urls')),
    path('disease_noti/', include('disease_noti.urls')),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)