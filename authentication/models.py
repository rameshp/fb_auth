# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DeleteStatus(models.Model):
    code = models.AutoField(primary_key=True)
    status = models.CharField(max_length=40)
