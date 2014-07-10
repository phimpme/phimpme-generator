#!/usr/bin/env python
# coding:utf-8

from django.db import models
import datetime
from django.contrib.auth.models import User
from Phimpme.settings import OUTPUT_PATH

class order(models.Model):
    "orders' records"
    order_related_user = models.ForeignKey(User)
    order_status = models.IntegerField(default=0)
    order_created_time = models.DateTimeField(auto_now=True)
    order_output_file = models.CharField(max_length=256)
    order_appname = models.CharField(max_length=256)
    order_fetures = models.CharField(max_length=2048)
    order_values = models.IntegerField(default=0)
    order_is_rebuild = models.BooleanField(default=False)
