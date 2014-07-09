#!/usr/bin/env python
# coding:utf-8

import thread
import time
from django.db import models
from Phimpme.apps.orders.models import order
from Phimpme.apps.usermgt.models import my_login_required
from django.core.context_processors import request
# Create your models here.

class appshop_paramters(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


def appshop_get_value(key):
    """
    """
    try:
        if key is None :
            raise Exception('key is None')
        else :
            param = appshop_paramters.objects.get(key=key)
            if param is None:
                raise Exception('key is not defined')
            else:
                if request.POST['value'] is not None:
                    param.value = request.POST['value']
                else :
                    raise Exception('no null value allowed')
    except Exception, e:
        return None


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

