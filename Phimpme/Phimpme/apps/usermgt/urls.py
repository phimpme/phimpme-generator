#!/usr/bin/env python
# coding:utf-8
'''
Created on 2014年6月28日

@author: tony
'''
from django.conf.urls import patterns, include, url
from Phimpme import settings
from Phimpme.apps.usermgt.views import *

urlpatterns = patterns('',
    url(r'^login/', usermgt_login),
    url(r'^register/', usermgt_register),
    url(r'^success/', prompt_success),
    url(r'^faild/', prompt_failed),
    # url('^index/', usermgt_index),
)

