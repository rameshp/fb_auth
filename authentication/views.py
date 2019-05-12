# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import requests
from django.shortcuts import (redirect, render)

config = {
    'client_id': '',
    'redirect_uri': 'http://localhost:8000/login_success',
    'client_secret': '',
    'fb_oauth_url': "https://www.facebook.com/v3.3/dialog/oauth"
}

def login_success(request):
    params = request.GET
    code = params['code']
    resp = requests.get("https://graph.facebook.com/v3.3/oauth/access_token",
                        params={'client_id': config['client_id'],
                                'redirect_uri': config['redirect_uri'],
                                'client_secret': config['client_secret'],
                                'code': code})
    response = resp.json()
    access_token = response['access_token']
    response = requests.get("https://graph.facebook.com/oauth/access_token",
                 params={'client_id':config['client_id'],
                         'client_secret': config['client_secret'],
                         'grant_type':'fb_exchange_token',
                         'fb_exchange_token': access_token}
                )
    response = response.json()
    access_token = response['access_token']
    request.session['access_token'] = access_token
    home_response = redirect('home')
    return home_response

def login(request):
    login_succ_path = 'login_success'
    return render(request, 'fb_login.html', {'client_id': config['client_id'], 
                  'login_succ_path': login_succ_path,
                  'fb_oauth_url':config['fb_oauth_url']})

def logout(request):
    session = request.session
    del session['access_token']
    del session['user_id']
    return render(request, 'logout.html') 