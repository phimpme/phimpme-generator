#!/usr/bin/env python
# coding:utf-8
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms

from django.contrib.auth.models import User
from Phimpme.apps.orders.models import order
from Phimpme.apps.usermgt.models import my_login_required
from Phimpme.apps.appshop.models import appshop_generate
from django.core.context_processors import request
# Create your views here.

@my_login_required
def orders_review(request):
    """
    {"result":"success","data":[{"id":"x","status":"x","refer":"","content":"1,2,3,4,4"},]}
    """
    try:
        i = 0
        user = request.user
        orders = order.objects.filter(order_related_user=user)
        rvar = '{"result":"success","data":[ '
        for o in orders:
            name = user.username + " s'APP " + o.order_appname
            if o.order_status == 0:
                status = 'waiting payment'
            elif o.order_status == 1:
                status = 'processing'
            else:
                status = 'complete'
            rvar += '{"id":"' + str(o.id) + '","status":"' + str(o.order_status) + '","refer":"' + str(o.order_output_file) + '","content":"' \
            + str(o.id) + ',' + name + ',' + str(o.order_values) + ',' + status + '"},'
            i = i + 1
        rvar = rvar[0:-1]
        rvar += ']}'
        return HttpResponse(rvar)
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"review order failed!%s"}' % e)


@my_login_required
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
        if request.method == 'POST':
            user = request.user
            order_fetures = ' '
            app_name = request.POST['app_name']
            if (request.POST['enable_choose_from_library'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.POST['enable_map'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.POST['enable_nfc'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.POST['enable_photo_capturing'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.POST['enable_photo_location_modification'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'
            if (request.POST['enable_photo_manipulation'] == 'on'):
                order_fetures += 'ENABLE_CHOOSE_FROM_LIBRARY,'

            # TODO : FIXME : generate real values
            order_values = 0

            order_fetures = order_fetures[0:-1]
            oa = order(\
                        order_related_user=user, order_status=0, \
                        order_appname=app_name, \
                        order_fetures=order_fetures, order_values=order_values)
            oa.save()
            return HttpResponse('{"result":"success","msgstr":"waiting payment"}')
        else:
            raise Exception('method is not POST ')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"ording failed!%s"}' % e)



@my_login_required
def orders_reconf(request):
    """
    """
    try:
        if request.method == 'POST':
            old_id = request.POST['id']
            old_order = order.objects.get(id=old_id)
            if old_order is not None:
                raise Exception('old order is not exist')
            else:
                new_fetures = ''
                old_order.fetures = new_fetures
                old_order.save()
        else :
            raise Exception('method is not post ')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"ording failed!%s"}' % e)

