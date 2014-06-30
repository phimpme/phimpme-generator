#!/usr/bin/env python
# coding:utf-8
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms

from django.contrib.auth.models import User
from Phimpme.apps.orders.models import order
# Create your views here.
def orders_review(request):
    """
    """
    try:
        user = request.user
        orders = order.objects.filter(order_related_user=user)
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"review order failed!%s"}' % e)



def orders_ordering(request):
    """
    "app_name":app_name,
    "enable_choose_from_library":on/None,
    "enable_map":on/None,
    "enable_nfc":on/None,
    "enable_photo_capturing":on/None,
    "enable_photo_location_modification":on/None,
    "enable_photo_manipulation":on/None
    """
    try:
        if request.method == 'GET':
            user = request.user
            order_fetures = ' '
            app_name = request.GET['app_name']
            if (request.GET['enable_choose_from_library'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.GET['enable_map'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.GET['enable_nfc'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.GET['enable_photo_capturing'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.GET['enable_photo_location_modification'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.GET['enable_photo_manipulation'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'

            order_fetures = order_fetures[0:-1]
            # TODO: FIXME:generate

            oa = order(\
                        order_related_user=user, order_status=0, \
                        order_appname=appname, \
                        order_fetures=order_fetures)
            oa.save()
            return HttpResponseRedirect('{"result":"success","msgstr":"processing"}')
        else:
            from logging import exception
            raise Exception('method is not get ')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"ording failed!%s"}' % e)



