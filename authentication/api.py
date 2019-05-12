import json
import requests

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from django.conf import settings
from users.db_api import check_user_status_and_add

FB_CONFIG = settings.FB_CONFIG


def login_required(func):
    """
    Decoratpr for login check
    """
    def inner_func(request):
        access_token = request.session.get('access_token')
        user_id = request.session.get('user_id')
        if not access_token:
            return redirect('login')
        if not user_id:
            fields = get_fb_fields(request, ['id', 'name'])
            user_id = fields.get('id')
            user_name = fields.get('name')
            request.session['user_id'] = user_id
            check_user_status_and_add(user_id=user_id, user_name=user_name)
        return func(request)
    return inner_func

def get_fb_fields(request, fields):
    """ Returns facebook fields """
    access_token = request.session.get('access_token')
    fields = ','.join(fields)
    response = requests.get('https://graph.facebook.com/me', 
                             params={'access_token': access_token,
                             'fields': fields})
    return response.json()

def get_secret_keys():
    """
    Returns secret keys stored in files
    """
    cache_obj = caches['default']
    fb_secret_settings = cache_obj.get('DB_SECRET_SETTINGS')
    if fb_secret_settings:
        return fb_secret_settings
    with open(FB_CONFIG['secret_file_path']) as fin:
        response = json.load(fin)
        cache_obj.set('DB_SECRET_SETTINGS', response)
        return response
