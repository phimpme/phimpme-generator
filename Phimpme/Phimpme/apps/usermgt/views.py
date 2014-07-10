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

'''
Created on 2014年6月28日

@author: tony
'''

# Create your views here.

def usermgt_login(request):
    """
    extend Django's login, just for js process, use json instead of http302
    """
    try:
        if request.method == 'GET':
            return render(request, 'login.html')
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
             raise Exception('username:[%s] login fail,authenticate failed' % (username))
        if user is not None and user.is_active:
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
        user = request.user
        logout(request)
        return render_to_response('success.html', {'msg':'have logout'})
    except Exception, e:
        return render_to_response('success.html', {'msg':'have logout'})

@login_required
def usermgt_changepwd(request):
    """
    """
    if request.method == 'POST':
        user = request.user
        op = request.POST['opassword']
        np1 = request.POST['password1']
        np2 = request.POST['password2']
        if np1 == np2 and np1 is not None:
            if user.check_password(op) == True:
                user.set_password(np1)
                return render_to_response('success.html', {'msg':'passwd change succesful'})
        else:
            return render_to_response('error.html', {'msg':'passwd change failed'})
    else :
        return render_to_response('changepwd.html', {'user':'%s' % request.user})

