#!/usr/bin/env python
# coding:utf-8
import datetime
from django.shortcuts import render_to_response, render
from django.template import Template, Context
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from Phimpme.apps.orders.models import order
from Phimpme.apps.appshop.models import appshop_generate
from django.core.context_processors import request
from Phimpme.apps.appshop.models import *
from Phimpme.apps.defray.views import defray_pay
# Create your views here.





def home(request):
    """index page ."""
    user = request.user
    if user is not None and user.is_anonymous() != True:
        return render_to_response('app_config.html', {'user': '%s' % request.user})
    else :
        return render_to_response('app_config.html', {})


@login_required
def order_opation_switch(request):
    """
     define which operation we support
    """
    id = request.POST['id']
    if request.POST['operation'] == 'pay':
        return defray_pay(request)
    elif request.POST['operation'] == 'reconf':
        return orders_reconf(request)
    elif request.POST['operation'] == 'delete':
         o = order.objects.get(id=id)
         if o is not None:
             o.order_status = -1
             o.save()
         return render_to_response('success.html', {'msg': 'delete OK', 'url':'cgi-bin/orders/review/'})
    else:
         return render_to_response('error.html', {'msg':'operation is not allowed', 'url':'cgi-bin/orders/review/'})

@login_required
def orders_review(request):
    """
    {"result":"success","data":[{"id":"x","status":"x","refer":"","content":"1,2,3,4,4"},]}
    """
    try:
        user = request.user
        orders = order.objects.filter(order_related_user=user).exclude(order_status=-1)
        return render_to_response('history.html', {'all_order':orders, 'user':user})
    except Exception, e:
        return render_to_response('error.html', {'msg':'%s' % e, 'url':'/'})



def orders_process(user, app_name, app_package, enables):
    oa = None
    order_values = int(appshop_get_value('first_build_price'))
    delta = int(appshop_get_value('order_expiry'))
    oas = order.objects.filter(order_related_user=user, order_appname=app_name)

    if oas is not None and len(oas) != 0 :
        oa = oas[0]
    if oa is None:
        oa = order(\
                    order_related_user=user, order_status=0, \
                    order_appname=app_name, order_package=app_package, \
                    order_fetures=str(enables), order_values=order_values)
        oa.order_created_time = datetime.datetime.now()
        oa.order_due_time = oa.order_created_time + datetime.timedelta(seconds=delta)
    else:
        due_time = oa.order_due_time
        if datetime.datetime.now() > due_time:
            order_values = int(appshop_get_value('rebuild_price'))
        else:
            order_values = 0
        oa = order(\
            order_related_user=user, order_status=0, \
            order_appname=app_name, \
            order_fetures=str(enables), order_values=order_values, \
            order_package=app_package, \
            order_due_time=due_time)
    oa.save()

@login_required
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
            app_name = request.POST['app_name']
            app_package = request.POST['app_package']
            enables = []
            for (k, v) in request.POST.items():
                if k.find('enable_') != -1:
                    enables.append(k.upper())
            orders_process(user, app_name, app_package, enables)
            return render(request, 'success.html', {'msg': 'waiting payment', 'url':'cgi-bin/orders/review/'})
        else:
            raise Exception('method is not POST ')
    except Exception, e:
       return render_to_response('error.html', {'msg':'%s' % e, 'url':'/'})




def orders_preordering(request):
    user = request.user
    if user is None or user.is_authenticated() == False:
        enables = []
        for (k, v) in request.POST.items():
            if k.find('enable_') != -1:
                enables.append(k.upper())
        request.session['app_name'] = request.POST['app_name']
        request.session['app_package'] = request.POST['app_package']
        request.session['enables'] = enables
    return orders_ordering(request)



@login_required
def orders_reconf(request):
    """
     reconf statemachine:

    """
    try:
        if request.method == 'POST':
            old_id = request.POST['id']
            old_order = order.objects.get(id=old_id)
            if old_order is None:
                raise Exception('old order is not exist')
            else:

                return render_to_response('app_config.html', {'user': '%s' % request.user, \
                                                              'appname':'%s' % old_order.order_appname, \
                                                              'app_package':old_order.order_package})
        else :
            raise Exception('method is not post ')
    except Exception, e:
        return render_to_response('error.html', {'msg':'%s' % e, 'url':'/'})
