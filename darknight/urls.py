"""darknight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django_urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog_urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.urls import path, include

from apps.backend import urls as backend_urls
from apps.dataapi import urls as dataapi_urls
from apps.front import urls as front_urls
from apps.front.views import page_not_found, page_err
from apps.postoperate import urls as postoperate_urls
from apps.userauth import urls as userauth_urls

urlpatterns = [
                  path('', include(front_urls)),
                  path('sitecms/', include(backend_urls)),
                  path('v1/api/', include(dataapi_urls)),
                  path('operate/', include(postoperate_urls)),
                  path('auth/', include(userauth_urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
handler500 = page_err
