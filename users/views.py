# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from authentication.api import login_required, get_fb_fields
from users.db_api import get_user

# Create your views here.


@login_required
def home(request):
    user_id = request.session.get('user_id')
    print user_id
    result = get_user(user_id)
    user_name = result['user_name']
    print result
    return render(request, 'home.html',
                  {'user_id': user_id, 'user_name': user_name})
