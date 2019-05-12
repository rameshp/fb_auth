# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

from django.http import HttpResponse
from django.shortcuts import (redirect, render)
from django.conf import settings
from authentication.api import  get_secret_keys
from users.db_api import disable_user
from authentication.models import DeleteStatus

FB_CONFIG = settings.FB_CONFIG

def login_success(request):
    """ Call back end point for fb after loggin in"""
    params = request.GET
    code = params['code']
    secret_keys = get_secret_keys()
    resp = requests.get(FB_CONFIG['token_url'],
                        params={'client_id': secret_keys['client_id'],
                                'redirect_uri': FB_CONFIG['redirect_uri'],
                                'client_secret': secret_keys['client_secret'],
                                'code': code})
    response = resp.json()
    access_token = response['access_token']
    response = requests.get(FB_CONFIG['token_url'],
                 params={'client_id':secret_keys['client_id'],
                         'client_secret': secret_keys['client_secret'],
                         'grant_type':'fb_exchange_token',
                         'fb_exchange_token': access_token}
                )
    response = response.json()
    access_token = response['access_token']
    request.session['access_token'] = access_token
    home_response = redirect('home')
    return home_response

def login(request):
    """ Loads fb login page """
    secret_keys = get_secret_keys()
    login_succ_path = 'login_success'
    return render(request, 'fb_login.html', {'client_id': secret_keys['client_id'], 
                  'login_succ_path': login_succ_path,
                  'fb_oauth_url':FB_CONFIG['oauth_url']})

def logout(request):
    """ Logsout page"""
    session = request.session
    del session['access_token']
    del session['user_id']
    return render(request, 'logout.html')

def deauth_callback(request):
    """ Call back for deauthentication """
    user_id = request.get('id')
    try:
        disable_user(user_id)
        status = "Successfully deleted"
    except:
        status = "Failed while deleting"
    ds = DeleteStatus(status=status)
    ds.save()
    code = ''
    url = FB_CONFIG['deauth_status']
    response = {'url': url, 'code': code}
    return HttpResponse(response)

def delete_status(request):
    """Returns delete app status """
    code = request.GET.get('code')
    ds = DeleteStatus.objects.filter(code=code)
    status = ''
    if ds:
        status = ds[0].status
    return HttpResponse(status)