#!/usr/bin/env python
# coding:utf-8


from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django import forms

from Phimpme.apps.orders.models import order
# Create your views here.


def defray_pay(request):
    """
    just tell the order-system that we have forked out enough money
    """
    user = request.user
    id = request.POST['id']
    orders = order.object.filter(id=id)
    for o in orders:
        o.order_status = 1

