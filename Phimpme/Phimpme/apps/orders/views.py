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
# Create your views here.

@my_login_required
def orders_review(request):
    """
    {"result":"success","data":[{"id":1,"status":0,"content":"1,2,3,4,4"},{"id":2,"statas":3,"content":"1,2,3,4,4"}]}
    """
    try:
        i = 0
        user = request.user
        orders = order.objects.filter(order_related_user=user)
        rvar = '{"result":"success","data":[ '
        for o in orders:
            name = user.username + " s App " + o.order_appname
            if o.order_status == 0:
                status = 'waiting payment'
            elif o.order_status == 1:
                status = 'processing'
            else:
                status = 'complete'
            rvar += '{"id":"' + str(i) + '","status":"' + str(o.order_status) + '","refer":"' + str(o.order_output_file.name) + '","content":"' \
            + str(o.id) + ',' + name + ', 0,' + status + '"},'
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

            order_fetures = order_fetures[0:-1]
            # TODO: FIXME:generate

            oa = order(\
                        order_related_user=user, order_status=0, \
                        order_appname=app_name, \
                        order_fetures=order_fetures)
            oa.save()
            return HttpResponse('{"result":"success","msgstr":"processing"}')
        else:
            raise Exception('method is not POST ')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"ording failed!%s"}' % e)



