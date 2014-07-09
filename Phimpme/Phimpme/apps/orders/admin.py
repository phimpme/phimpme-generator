#!/usr/bin/env python
# coding:utf-8

from django.contrib import admin
from Phimpme.apps.orders.models import order

# Register your models here.

class orderAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('id', 'order_related_user', 'order_values', 'order_appname', 'order_created_time', 'order_fetures')



admin.site.register(order, orderAdmin)
