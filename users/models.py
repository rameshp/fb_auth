# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	user_id = models.CharField(primary_key=True, max_length=20)
	user_name = models.CharField(max_length=50, null=False)
	other_field1 = models.CharField(max_length=50, null=True)
	other_field2 = models.CharField(max_length=50, null=True)
	is_active = models.BooleanField(default=True)
