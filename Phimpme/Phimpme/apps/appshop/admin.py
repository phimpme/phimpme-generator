#!/usr/bin/env python
# coding:utf-8


from django.contrib import admin

from Phimpme.apps.appshop.models import appshop_paramters

# Register your models here.


class appshopAdmin(admin.ModelAdmin):
	"""
	"""
	list_display = ('id', 'key_name', 'value')

# add appshop_paramters model to adminsystem
admin.site.register(appshop_paramters, appshopAdmin)

