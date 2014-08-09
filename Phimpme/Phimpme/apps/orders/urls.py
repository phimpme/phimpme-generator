#!/usr/bin/env python
# coding:utf-8
'''
Created on 2014年6月28日

@author: tony
'''
from django.conf.urls import patterns, url

from Phimpme.apps.orders.views import *


urlpatterns = patterns('',
                       url(r'^order/', orders_preordering),
                       url(r'^review/', orders_review),
                       url(r'^history/', order_operation_switch)
)

