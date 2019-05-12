from django.http import HttpResponse
import requests
from django.shortcuts import redirect, render


def login_required(func):
    def inner_func(request):
        access_token = request.session.get('access_token')
        user_id = request.session.get('user_id')
        if not access_token:
            return redirect('login')
        if not user_id:
            fields = get_fb_fields(request, ['id', 'name'])
            request.session.user_id = fields.get('id')
        return func(request)
    return inner_func

def get_fb_fields(request, fields):
    access_token = request.session.get('access_token')
    response = requests.get('https://graph.facebook.com/me', 
                                     params={'access_token': access_token,
                                     'fields': 'id,name'})
    return response.json()