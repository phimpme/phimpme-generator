#!/usr/bin/env python
# coding:utf-8

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from Phimpme.apps.orders.views import orders_process
from Phimpme.apps.usermgt.models import passwd_regain


from Phimpme.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import random
import datetime
import time, string
'''
Created on 2014年6月28日

@author: tony
'''

# Create your views here.


def usermgt_check_timeout():
    """
    """
    t_timeout = datetime.datetime.now() - datetime.timedelta(hours=1)
    regains = passwd_regain.objects.filter(date__lt=t_timeout)
    for regain in regains:
        regain.delete()

def usermgt_login(request):
    """
    extend Django's login, just for js process, use json instead of http302
    """
    try:
        usermgt_check_timeout()
        if request.method == 'GET':
            return render(request, 'login.html')
        else:
            username = request.POST.get('username', '').strip('"\' ')
            userpwd = request.POST.get('userpwd', '').strip('"\' ')
        if username is None or username == '':
            raise Exception('Null username is not allowed')

        user = authenticate(username=username, password=userpwd)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                raise Exception('username:[%s] login fail,no active' % (username))
        else:
             raise Exception('username:[%s] login fail,authenticate failed' % (username))
        if user is not None and user.is_active:
            if request.session.get('app_name', default=None) is not None :
                orders_process(request.user, request.session['app_name'], request.session['app_package'], request.session['enables'])
                request.session['app_name'] = None
                return render(request, 'success.html', {'msg': 'now will continue your order...', 'url':'cgi-bin/orders/review/'})
            return render(request, 'app_config.html', {'user': '%s' % request.user})
        else:
            raise Exception('login failed, user is not active')
    except Exception, e:
        return render(request, 'error.html', {'msg':'%s' % e})



def usermgt_register(request):
    """
    now only need three element : username/userpwd/email
    """
    try:
        usermgt_check_timeout()
        if request.method == 'POST':
            username = request.POST['email']
            userpwd = request.POST['userpwd']
            email = request.POST['email']
            if username is not None and userpwd is not None and email is not None:
                user = User.objects.filter(username=username)
                if user is None or len(user) == 0:
                    user = User(username=username, email=email)
                    user.set_password(userpwd)
                else:
                    raise Exception('user have registed')
                user.save()
                return HttpResponse('{"result":"success","msgstr":"registerd OK"}')
            else:
                raise Exception('less info required ')
        else:
             raise Exception('method is not POST')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"%s"}' % e)


@login_required
def usermgt_logout(request):
    """
    logout is always successs
    """
    try:
        usermgt_check_timeout()
        user = request.user
        logout(request)
        return render_to_response('success.html', {'msg':'have logout'})
    except Exception, e:
        return render_to_response('success.html', {'msg':'have logout'})


def usermgt_changepwd(request):
    if request.method == 'POST':
        active_key = request.POST.get('active_key', default=None)
        if active_key is not None:
            return usermgt_changepwd_regain(request, active_key)
    return usermgt_changepwd_normal(request)


def usermgt_changepwd_regain(request, active_key):
    """
    """
    p1 = request.POST.get('password1', default=None)
    p2 = request.POST.get('password2', default=None)

    if p1 is not None and p2 is not None and p1 == p2:
        regain = passwd_regain.objects.get(active_key=active_key)
        if regain is not None:
            user = regain.user
            user.set_password(p1)
            user.save()
            regain.delete()
            return render_to_response('success.html', {'msg':'passwd change succesful'})
    return render_to_response('error.html', {'msg':'passwd change failed'})

@login_required
def usermgt_changepwd_normal(request):
    """
    """
    if request.method == 'POST':
        user = request.user
        op = request.POST['opassword']
        np1 = request.POST['password1']
        np2 = request.POST['password2']
        if np1 == np2 and np1 is not None and np1 != '':
            if user.check_password(op) == True:
                user.set_password(np1)
                user.save()
                return render_to_response('success.html', {'msg':'passwd change succesful'})
        return render_to_response('error.html', {'msg':'passwd change failed'})
    else :
        return render_to_response('changepwd.html', {'user':'%s' % request.user})



@login_required
def usermgt_changemail(request):
    """
    """
    if request.method == 'POST':
        user = request.user
        passwd = request.POST.get('password', default=None)
        email = request.POST.get('email', default=None)
        if passwd is not None and email is not None:
            if user.check_password(passwd) == True:
                user.username = email
                user.email = email
                user.save()
                return render_to_response('success.html', {'msg':'email change succesful'})
        return render_to_response('error.html', {'msg':'email change failed'})
    else:
        return render_to_response('changemail.html', {'user':'%s' % request.user})



def usermgt_sendmail(to_users, key):
    send_mail('Reset Your Password!', 'click the url http://192.168.56.101:8000/cgi-bin/usermgt/regain/?active_key=%s' % key,
                             EMAIL_HOST_USER, to_users)
    thread.exit_thread()

def usermgt_regain(request):
    """
    """
    try:
        if request.method == 'POST':
            user = request.user
            if user.is_authenticated() != True:
                # send mail
                email = request.POST.get('email', default=None)
                if email is None:
                    raise Exception('email must not be none')
                user = User.objects.get(email=email)
                if user is not None:
                    s = passwd_regain(user=user, active_key=random.randint(0, int(time.mktime(time.gmtime()))))
                    thread.start_new_thread(usermgt_sendmail, ([user.email], s.active_key))
                    s.save()
                    return render_to_response('success.html', {'msg':'please check your Email Inbox...'})
                else :
                    return render_to_response('error.html', {'msg':'email have not been registered'})
            else:
                return render_to_response('error.html', {'msg':'you have logged in , please logout first'})
        else:
            active_key = request.GET.get('active_key', default=None)
            if active_key is not None:
                regain = passwd_regain.objects.get(active_key=active_key)
                if regain is not None:
                    user = regain.user
                    return render_to_response('changepwd.html', {'user':user, 'active_key':active_key})
            return render_to_response('forgetpasswd.html', {})
    except Exception, e:
        return render(request, 'error.html', {'msg':'%s' % e})


