# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

# Create your models here.
from django.db import models

class Test(models.Model):
    script_name = models.CharField(u'脚本名称',max_length=100)
    params_name = models.CharField(u'参数名称',max_length=100)
    params = models.TextField(u'参数列表',blank=True)
    #history = models.TextField(u'历史操作记录', blank=True)

    # def __unicode__(self):
    #     return self.scriptname

class Contact(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    # contact = models.ForeignKey(Contact)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'polls_tag'

class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)