#!/usr/bin/env python
# coding:utf-8
'''
Created on 2014年6月28日

@author: tony
'''
from django.conf.urls import patterns, url

from Phimpme.apps.usermgt.views import *


urlpatterns = patterns('',
                       url(r'^login/', usermgt_login),
                       url(r'^register/', usermgt_register),
                       url(r'^changepwd/', usermgt_changepwd),
                       url(r'^changemail/', usermgt_changemail),
                       url(r'^logout/', usermgt_logout),
                       url(r'^regain/', usermgt_regain),
)

