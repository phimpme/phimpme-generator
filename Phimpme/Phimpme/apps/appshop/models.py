#!/usr/bin/env python
# coding:utf-8

import thread
import time
from django.db import models
from Phimpme.apps.orders.models import order
from Phimpme.apps.usermgt.models import my_login_required
# Create your models here.



def generate_thread(id, t):
    """
    TODO:FIXME: porting real generate interface
        call generate(app_name, app_logo, enables) instead
    """
    time.sleep(t)
    o = order.objects.get(id=id)
    if o is None:
        raise Exceptions('order %s be not found' % (id))
    else:
        o.order_status = 2
        # TODO: FIXME :
        o.order_output_file = '/static/output_path/output_example'
        o.save()
    thread.exit_thread()

@my_login_required
def appshop_generate(request, o):
    """
    """
    if order is None:
        return False
    else :
        thread.start_new_thread(generate_thread, (o.id, 30))
        return True

