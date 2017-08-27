#encoding:utf-8
#from __future__ import unicode_literals

import json
from datetime import datetime
from django.utils.html import format_html
from django.contrib import admin
from polls.models import Tag, Test, Contact
from django.contrib import messages


# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email')  # list
    search_fields = ('name',)
    fieldsets = (
        ['Main', {
            'fields': ('name', 'email'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': ('age',),
        }]

    )
    def log_change(self, request, object, message):
        newmessage = "xxxx" # 将消息改写为xxx
        print request, "***", object, "****", message
        print type(request), "***", type(object), "****", type(message)
        super(ContactAdmin, self).log_change(request, object, message)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'edit_name')
    search_fields = ('id',)

    def log_change(self, request, object, message):
        print 'aaaaa', Tag.objects.get(id=3)
        print request, "***", object, "****", message
        print type(request), "***", type(object), "****", type(message)
        super(TagAdmin, self).log_change(request, object, message)

    def save_model(self, request, obj, form, change):
        id = request.path.split('/')[-3]
        print id
        print request, obj, form, change
        obj.save()

    def edit_name(self, obj):
        return ("%s + %s" % (obj.id, obj.name)).upper()
        edit_name.short_description = 'editName'

class TestAdmin(admin.ModelAdmin):
    list_display = ('id','script_name', 'params_name', 'resolve_param')
    search_fields = ('script_name', 'params_name')
    ordering = ['id']
    raw_infos = {}
    signal = False

    def log_change(self, request, object, message):
        if self.signal:
            self.signal = False
            return
        self.message_user(request, "hello world")
        id = request.path.split('/')[-3]
        print '--------------------------', Test.objects.get(id=id).__dict__
        print self.raw_infos

        info = Test.objects.get(id=id).__dict__
        raw_info = self.raw_infos

        record = {}
        record['add'] = []
        record['edit'] = []
        record['delete'] = []
        if not raw_info['params'] == info['params']:
            print "edit_log"
            if not (self.is_json(raw_info['params']) and self.is_json(info['params'])):
                record['edit'].append(('params', raw_info, info))
            else:
                raw_info = json.loads(raw_info['params'])
                info = json.loads(info['params'])
                if isinstance(raw_info, dict) and isinstance(info, dict):
                    self.compare_dict(record, raw_info, info)
                    self.is_add(record, raw_info, info)
                else:
                    record['edit'].append(('params', raw_info, info))

        message = ''
        print type(message)
        for item in ['add', 'edit', 'delete']:
            if record[item]:
                message = message + self.param_to_str(item, record[item]) + ';'
                print type(message)

        print request, "***", object, "****", message
        print type(request), "***", type(object), "****", type(message)
        super(TestAdmin, self).log_change(request, object, message)
        print "edit_log/"

    def save_model(self, request, obj, form, change):
        print "=========="
        params = obj.__dict__['params']
        print type(params)
        if not self.is_json(params):
            # self.message_user(request, "hello world")
             # messages.add_message(request, messages.ERROR, "请输入正确的json格式数据")
            messages.set_level(request, messages.ERROR)
            messages.error(request, "请输入正确的json格式数据")
            self.signal = True
            return
        id = request.path.split('/')[-3]
        try:
            raw_info = Test.objects.get(id=id)
        except ValueError, e:
            print "error"
        else:
            raw_info = raw_info.__dict__
            self.raw_infos = raw_info
        finally:
            obj.save()

    def resolve_param(self, obj):
        param = obj.params
        if self.is_json(param):
            return format_html(self.format_json(json.loads(param)))
            # if isinstance(json.loads(param), dict):
            #     return format_html(self.format_dict(json.loads(param)))

        return format_html(self.format_str(param))
    resolve_param.short_description = '参数列表'

    @staticmethod
    def is_json(myjson):
        if isinstance(myjson, str) or isinstance(myjson, unicode):  # 首先判断变量是否为字符串
            try:
                json.loads(str(myjson), encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False

    @staticmethod
    def format_dict(mydict):
        print mydict, type(mydict)
        s = ''
        s = s + '<table border="1">'
        for key, value in mydict.items():
            s = s + '<tr border="1">'
            if isinstance(value, dict):
                s = s + ('<td>%s</td><td>%s</td>' % (key, TestAdmin.format_dict(value)))
                # print format(value)
            elif isinstance(value, list):
                s = s + ('<td>%s</td><td style="word-break: break-all;">' % key)
                for element in value:
                    if isinstance(element, dict):
                        s = s + TestAdmin.format_dict(element);
                    else:
                        s = s + str(element) + ','
                s = s + ('</td>')
            else:
                s = s + ('<td>%s</td><td style="word-break: break-all;">%s</td>' % (key, value))
            s = s + '</tr>'
        s = s + '</table>'
        return s

    @staticmethod
    def format_json(myjson):
        print myjson, type(myjson)
        if isinstance(myjson, list):
            s = '<table border="1">'
            temp = ''
            for element in myjson:
                if not isinstance(element, list) and not isinstance(element, dict):
                    temp = temp + str(element) + ','
                else:
                    s = s + '<tr><td>'
                    s = s + TestAdmin.format_json(element)
                    s = s + '</td></tr>'
            s = s + '<tr><td style="word-break: break-all;">' + temp[:-1] + '</td></tr>'
            s = s + '</table>'
            return s
        elif isinstance(myjson, dict):
            s = ''
            s = s + '<table border="1">'
            for key, value in myjson.items():
                s = s + '<tr><td>' + key + '</td><td>'
                s = s + TestAdmin.format_json(value)
                s = s + '</td></tr>'
            s = s + '</table>'
            return s
        else:
            return str(myjson)

    @staticmethod
    def format_str(strs):
        return '<table><tr><td style="word-break: break-all;">' + str(strs) + '</td></tr></table>'

    @staticmethod
    def compare_dict(info, be, af):
        for key in be:
            if key not in af.keys():
                print "删除"
                info['delete'].append(key)
            elif be[key] != af[key]:
                print '', be[key], type(be[key])
                if isinstance(be[key], dict):
                    TestAdmin.compare_dict(info, be[key], af[key])
                    TestAdmin.is_add(info, be[key], af[key])
                else:
                    info['edit'].append((key, be[key], af[key]))

    @staticmethod
    def is_add(info, be, af):
        for key in af:
            if key not in be.keys():
                print "新增"
                info['add'].append(key)

    @staticmethod
    def param_to_str(key, value):
        if key == 'add':
            print type('新增参数字段:'), "****"
            return '新增参数字段:' + json.dumps(value)
        if key == 'delete':
            print type('新增参数字段:'), "****"
            return '删除参数字段:' + json.dumps(value)
        if key == 'edit':
            s = str('')
            for info in value:
                s = s + '修改字段' + json.dumps(info[0]) + '从' + str(info[1]) + '到' + str(info[2]) + ','
            s = s[:-1]
            return s

admin.site.register(Contact, ContactAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Tag, TagAdmin)