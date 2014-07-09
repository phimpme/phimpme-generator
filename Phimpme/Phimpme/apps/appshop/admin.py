#!/usr/bin/env python
# coding:utf-8


from django.contrib import admin
from Phimpme.apps.appshop.models import appshop_paramters
# Register your models here.


class appshopAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('id', 'key', 'value')

admin.site.register(appshop_paramters, appshopAdmin)

