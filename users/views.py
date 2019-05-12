# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from authentication.api import login_required, get_fb_fields

# Create your views here.


@login_required
def home(request):
    fields = get_fb_fields(request, ['id', 'name'])
    return HttpResponse("Hello, world. You're at the polls index{}".format(fields))
