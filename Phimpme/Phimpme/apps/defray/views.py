#!/usr/bin/env python
# coding:utf-8


from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django import forms
from Phimpme.apps.usermgt.models import my_login_required
from Phimpme.apps.orders.models import order
from Phimpme.apps.appshop.models import appshop_generate
# Create your views here.

@my_login_required
def defray_pay(request):
    """
    just tell the order-system that we have forked out enough money
    """
    try:
        if request.method == 'POST':
            user = request.user
            id = request.POST['id']
            o = order.objects.get(id=id)
            # TODO:FIXME: porting real defray interface


            if o is not None:
                if appshop_generate(request, o) is True:
                    o.order_status = 1
                    o.save()
                return HttpResponse('{"result":"success","msgstr":"processing %s"}' % id)
            return HttpResponse('{"result":"success","msgstr":"no such id %s"}' % id)
        else:
            raise Exception('method is not POST')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"ording failed!%s %s"}' % (e, id))
