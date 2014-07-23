#!/usr/bin/env python
# coding:utf-8


from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django import forms
from Phimpme.apps.orders.models import order
from Phimpme.apps.appshop.models import appshop_generate
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required
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
                try:
                    if appshop_generate(request, o) is True:
                        o.order_status = 1
                        o.save()
                        return render_to_response('success.html', {'url':'cgi-bin/orders/review/'})
                except Exception, e:
                    o.order_status = 0xf
                    o.save()
                    return render_to_response('error.html', {'msg':'generate Failed(%s)' % e, 'url':'cgi-bin/orders/review/'})

            raise Exception('no such id %s' % id)
        else:
            raise Exception('method is not POST')
    except Exception, e:
        return render_to_response('error.html', {'msg':'%s' % e, 'url':'cgi-bin/orders/review/'})
