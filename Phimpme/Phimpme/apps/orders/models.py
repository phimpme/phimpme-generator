#!/usr/bin/env python
# coding:utf-8

from django.db import models
from django.contrib.auth.models import User

from Phimpme.settings import OUTPUT_PATH


class order(models.Model):
	"orders' records"
	order_related_user = models.ForeignKey(User)
	order_status = models.IntegerField(default=0)
	order_created_time = models.DateTimeField(auto_now_add=True)
	order_output_file = models.CharField(max_length=256)
	order_appname = models.CharField(max_length=256)
	order_package = models.CharField(max_length=256)
	order_features = models.CharField(max_length=2048)
	order_values = models.IntegerField(default=0)
	order_due_time = models.DateTimeField()
	order_is_rebuild = models.BooleanField(default=False)
	order_payment_id = models.CharField(max_length=256)
	order_payer_id = models.CharField(max_length=256)
	order_logo = models.FileField(upload_to=OUTPUT_PATH)  # parameter 'upload_to' must be relative path
	order_background = models.FileField(upload_to=OUTPUT_PATH)




