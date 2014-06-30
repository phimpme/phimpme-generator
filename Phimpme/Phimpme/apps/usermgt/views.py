#!/usr/bin/env python
# coding:utf-8
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms

from django.contrib.auth.models import User

# Create your views here.


def usermgt_index(request):
    """
    """
    return render_to_response('login.html', {})

def usermgt_login(request):
    """
    """
    try:
        username = request.GET['username']
        m = User.objects.get(username=username)
        if m.password == request.GET['userpwd']:
            request.session['member_id'] = m.id
            return HttpResponseRedirect('{"result":"success","msgstr":"/you-are-logged-in/"}')
    except User.DoesNotExist:
        return HttpResponse('{"result":"error","msgstr":"Your username and password do not match."}')

def usermgt_register(request):
    """
    """
    try:
        username = request.GET['username']
        userpwd = request.GET['userpwd']
        email = request.GET['email']
        if username is not None and userpwd is not None and email is not None:
            user = User.objects.filter(username=username)
            if user is None or len(user) == 0:
                user = User(username=username, password=userpwd, email=email)
            else:
                raise Exception('user have registed')
            user.save()
            return HttpResponseRedirect('{"result":"success","msgstr":"registerd OK"}')
        else:
            raise Exception('less info required ')
    except Exception, e:
        return HttpResponse('{"result":"error","msgstr":"%s"}' % e)

def prompt_success(request):
    """
    """

def prompt_failed(request):
    """
    """

