#!/usr/bin/env python
# coding:utf-8


from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django import forms
from Phimpme.apps.orders.models import order
from Phimpme.apps.appshop.models import appshop_generate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

import paypalrestsdk
from paypalrestsdk import Payment
import logging

from Phimpme.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, DOMAIN_NAME


# Include Headers and Content by setting logging level to DEBUG, particularly for
# Paypal-Debug-Id if requesting PayPal Merchant Technical Services for support
logging.basicConfig(level=logging.INFO)


# Create your views here.
paypalrestsdk.configure({
            "mode": PAYPAL_MODE,
            "client_id": PAYPAL_CLIENT_ID,
            "client_secret": PAYPAL_CLIENT_SECRET })
@login_required
def paypal_create(request):
    """
     Paypal > Create a Payment
    """
    try:
        if request.method == 'POST':
            user = request.user
            id = request.POST['id']
            o = order.objects.get(id=id)

            if o is None:
                raise Exception('app do not exist ')

            payment = Payment({
              "intent":  "sale",

              # ###Payer
              # A resource representing a Payer that funds a payment
              # Payment Method as 'paypal'
              "payer":  {
                "payment_method":  "paypal" },

              # ###Redirect URLs
              "redirect_urls": {
                "return_url": "http://%s/cgi-bin/defray/execute/" % DOMAIN_NAME,
                "cancel_url": "http://%s/cgi-bin/defray/execute_failed/" % DOMAIN_NAME },

              # ###Transaction
              # A transaction defines the contract of a
              # payment - what is the payment for and who
              # is fulfilling it.
              "transactions":  [ {

                # ### ItemList
                "item_list": {
                  "items": [{
                    "name": "%s-%s" % (o.order_appname, o.order_package),
                    "sku": "app",
                    "price": "%s" % o.order_values,
                    "currency": "USD",
                    "quantity": 1 }]},

                # ###Amount
                # Let's you specify a payment amount.
                "amount":  {
                  "total": "%s" % o.order_values,
                  "currency":  "USD" },
                "description":  "This is the payment for Phimpme APP." } ] })

            # Create Payment and return status
            if payment.create():
                print("Payment[%s] created successfully" % (payment.id))
                request.session['payment_id'] = payment.id
                o.order_payment_id = payment.id
                o.save()
                # Redirect the user to given approval url
                for link in payment.links:
                    if link.method == "REDIRECT":
                        redirect_url = link.href
                        print("Redirect for approval: %s" % (redirect_url))
                return HttpResponseRedirect(redirect_url)
            else:
                print("Error while creating payment:")
                raise Exception(payment.error)
        else :
            raise Exception('operation is not allowed ')
    except Exception, e:
        return render_to_response('error.html', {'msg':'%s' % e})


@login_required
def paypal_execute(request):
    """
    Execute a Payment
    """
    try:
        payment_id = request.session.get('payment_id', default=None)
        payer_id = request.GET['PayerID']

        payment = paypalrestsdk.Payment.find(payment_id)
        payment_name = payment.transactions[0].item_list.items[0].name

        if payment.execute({"payer_id": payer_id}):
            # the payment has been accepted
            try:
                o = order.objects.get(order_payment_id=payment_id)
                o.order_payer_id = payer_id
                o.save()

                if appshop_generate(request, o) is True:
                    o.order_status = 1
                    o.save()
                    return render_to_response('success.html', {'msg':'pay success', 'url':'cgi-bin/orders/review/'})
            except Exception, e:
                o.order_status = 4
                o.save()
                return render_to_response('error.html', {'msg':'pay success but generate Failed(%s)' % e, 'url':'cgi-bin/orders/review/'})
        else:
            # the payment is not valid
            return render_to_response('error.html', {'msg':'pay failed'})
    except Exception, e:
        return render_to_response('error.html', {'msg':'%s' % e})



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
