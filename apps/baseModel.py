# -*- coding: utf-8 -*-
# @Time    : 2020/5/23 19:22
# @Author  : dearMrYang
# @File    : baseModel.py
# @Software: PyCharm
from django.db import models


class BaseModel(models.Model):
    is_del = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
