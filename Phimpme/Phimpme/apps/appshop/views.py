#!/usr/bin/env python
# coding:utf-8


from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django import forms
from Phimpme.apps.usermgt.models import my_login_required
from Phimpme.apps.orders.models import order
# Create your views here.
@my_login_required
def appshop_generate(request):
    
    
    