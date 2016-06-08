#!/usr/bin/python
# -*- coding: utf-8 -*-

"""seastone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

import marina.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', marina.views.berths, name='berths'),
    url(r'^demo$', marina.views.map_demo, name='map-demo'),
    url(r'pier/add/$', marina.views.PierCreate.as_view(), name='pier-add'),
    url(r'pier/(?P<pk>[0-9]+)/$', marina.views.PierUpdate.as_view(), name='pier-update'),
    url(r'pier/(?P<pk>[0-9]+)/delete/$', marina.views.PierDelete.as_view(), name='pier-delete'),
    url(r'berth/add/$', marina.views.BerthCreate.as_view(), name='berth-add'),
    url(r'berth/(?P<pk>[0-9]+)/$', marina.views.BerthUpdate.as_view(), name='berth-update'),
    url(r'berth/(?P<pk>[0-9]+)/delete/$', marina.views.BerthDelete.as_view(), name='berth-delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
