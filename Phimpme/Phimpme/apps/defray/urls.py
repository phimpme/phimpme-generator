#!/usr/bin/env python
# coding:utf-8

from django.conf.urls import patterns

from Phimpme.apps.defray.views import *

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Phimpme.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       (r'^create/$', paypal_create),
                       (r'^execute/$', paypal_execute),
)
