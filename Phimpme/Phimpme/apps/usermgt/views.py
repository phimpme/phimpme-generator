#!/usr/bin/env python
# coding:utf-8

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms

from django.contrib.auth.models import User

# Create your views here.

def _login_callback(request, str_):
    if request.method == 'GET':
        return 'loginCallBack(%s)' % str_
    else:
        return str_


def usermgt_login(request):
    try:
        if request.method == 'GET':
            username = request.GET.get('username', '').strip('"\' ')
            userpwd = request.GET.get('userpwd', '').strip('"\' ')
        else:
            username = request.POST.get('username', '').strip('"\' ')
            userpwd = request.POST.get('userpwd', '').strip('"\' ')
        if username is None or username == '':
            return HttpResponse(_login_callback(request, '{"result":"error","errormsg":"userid or password is null"}'))

        user = authenticate(username=username, password=userpwd)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                raise Exception('username:[%s] login fail,no active' % (username))
        else:
             raise Exception('username:[%s] login fail,no find user' % (username))
        if user is not None and user.is_active:
            ret = _login_callback(request, '{"result":"success"}')
            return HttpResponse(ret)
        else:
            return HttpResponse(_login_callback(request, '{"result":"error","errmsg":"password error"}'))
    except Exception, e:
        return HttpResponse(_login_callback(request, '{"result":"error","errmsg":"password error%s"}' % e))


def user_logout(request):
    try:
        user = request.user
        logout(request)
        return HttpResponse('{"result":"success"}')
    except Exception, e:
        EXCEPTION(e)
        return HttpResponse('{"result":"success"}')



def usermgt_register(request):
    """
    """
    try:
        if request.method == 'POST':
            username = request.POST['username']
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



def usermgt_logout(request):
    """
    """
    try:
        user = request.user
        logout(request)
        return render_to_response('success.html', {})
    except Exception, e:
        return render_to_response('success.html', {})

