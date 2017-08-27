# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from models import BlogsPost
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Register your models here.

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class MyJsonEncoder(json.JSONEncoder):
    def encode(self, obj):
        obj = map_dict(obj, func=lambda k, v, pkeys: (k, v), atom_op=bigint2str)
        return json.JSONEncoder.encode(self, obj)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'resolve_param', 'timestamp')

    # def resolve_param(self, obj):
    #     param = obj.body
    #     if is_json(param):
    #         return format_html(format_json(json.loads(param)))
    #     return format_html(format_str(param))
    def resolve_param(self, obj):
        #return u'<table><tr><td>xxxxx</td><td>qqqq</td></tr><tr><td>asdfasf</td></tr></table>'
        print obj.body
        print json.dumps(obj.body, cls=CJsonEncoder)
        return '<pre json-data=1>"%s"</pre>' % (json.dumps(obj.body, cls=CJsonEncoder))
    resolve_param.short_description = '参数列表'
    resolve_param.allow_tags = True

def is_json(myjson):
    if isinstance(myjson, str) or isinstance(myjson, unicode):  # 首先判断变量是否为字符串
        try:
            json.loads(str(myjson), encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def format_json(myjson):
    print myjson, type(myjson)
    if not myjson:
        return ''
    if isinstance(myjson, list):
        s = '<table border="1">'
        temp = ''
        for element in myjson:
            if not isinstance(element, list) and not isinstance(element, dict):
                temp = temp + str(element) + ','
            else:
                s = s + '<tr><td>'
                s = s + format_json(element)
                s = s + '</td></tr>'
        if temp:
            s = s + '<tr><td style="word-break: break-all;">' + temp[:-1] + '</td></tr>'
        s = s + '</table>'
        return s
    elif isinstance(myjson, dict):
        s = ''
        s = s + '<table border="1">'
        for key, value in myjson.items():
            s = s + '<tr><td>' + key + '</td><td>'
            s = s + format_json(value)
            s = s + '</td></tr>'
        s = s + '</table>'
        return s
    else:
        return str(myjson)

def format_str(str):
    return '<table><tr><td style="word-break: break-all;">' + str + '</td></tr></table>'

admin.site.register(BlogsPost, BlogPostAdmin)