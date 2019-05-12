from django.http import HttpResponse
import requests
from django.shortcuts import redirect, render
from users.db_api import check_user_status_and_add


def login_required(func):
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
    access_token = request.session.get('access_token')
    response = requests.get('https://graph.facebook.com/me', 
                             params={'access_token': access_token,
                             'fields': 'id,name'})
    return response.json()