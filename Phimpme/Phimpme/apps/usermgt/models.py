#!/usr/bin/env python
# coding:utf-8
from django.db import models
from django.contrib.auth.models import User


class passwd_regain(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	active_key = models.CharField(max_length=256)