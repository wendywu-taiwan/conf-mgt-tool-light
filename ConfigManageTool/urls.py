"""ConfigManageTool URL Configuration

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
from django.urls import path
from ConfigManageTool import settings
from django.conf.urls import url, include
from django.contrib import admin


def add_url_prefix():
    return settings.URL_PRE_PATH + "ConfigManageTool/"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path(add_url_prefix() + 'accounts/', include('django.contrib.auth.urls')),
    path(add_url_prefix(), include('RulesetComparer.urls')),
    path(add_url_prefix(), include('permission.urls')),
    path(add_url_prefix(), include('shared_storage.urls')),
]
