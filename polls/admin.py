#encoding:utf-8
#from __future__ import unicode_literals

import json
from datetime import datetime
from django.utils.html import format_html
from django.contrib import admin
from polls.models import Tag, Test, Contact
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
    list_display = ('scriptname', 'paramname', 'resolve_param')
    search_fields = ('scriptname', 'paramname')
    ordering = ['scriptname']
    raw_infos = {}

    def log_change(self, request, object, message):
        self.message_user(request, "hello world")
        # newmessage = "xxxx" # 将消息改写为xxx
        id = request.path.split('/')[-3]
        print '--------------------------', Test.objects.get(id=id).__dict__
        print self.raw_infos

        info = Test.objects.get(id=id).__dict__
        raw_info = self.raw_infos

        record = {}
        record['add'] = []
        record['edit'] = []
        record['delete'] = []
        if not raw_info['param'] == info['param']:
            print "edit_log"
            raw_info = json.loads(raw_info['param'])
            info = json.loads(info['param'])
            if not isinstance(raw_info, dict):
                record['edit'].append(('param', raw_info, info))
            else:
                compare_dict(record, raw_info, info)
                is_add(record, raw_info, info)

        message = ''
        message = str(message)
        print type(message)
        for item in ['add', 'edit', 'delete']:
            if record[item]:
                message = message + param_to_str(item, record[item]) + ';'
                print type(message)

        print request, "***", object, "****", message
        print type(request), "***", type(object), "****", type(message)
        super(TestAdmin, self).log_change(request, object, message)
        print "edit_log/"

    def save_model(self, request, obj, form, change):
        info = request.POST['param']
        if is_json(info):
            print 'yes'
        else:
            print 'no'
        print change
        id = request.path.split('/')[-3]
        raw_info = {}
        print 'aaaaa', id
        try:
            raw_info = Test.objects.get(id=id)
        except ValueError, e:
            print "新建记录"
            obj.__dict__['history'] = '新建参数'
        else:
            raw_info = raw_info.__dict__
            self.raw_infos = raw_info
            # info = request.POST
            # record = {}
            # record['add'] = []
            # record['edit'] = []
            # record['delete'] = []
            # now = datetime.now()
            # record['time'] = ("%s/%s/%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second))
            # if not raw_info['param'] == info['param']:
            #     print "edit"
            #     raw_info = json.loads(raw_info['param'])
            #     info = json.loads(info['param'])
            #     if not isinstance(raw_info, dict):
            #         record['edit'].append(('param', raw_info, info))
            #     else:
            #         compare_dict(record, raw_info, info)
            #         is_add(record, raw_info, info)
            #
            # print '===='
            # print record
            # obj.__dict__['history'] = edit_history(obj.__dict__['history'], record)
            # print '===='
            # print request.POST, "--", obj, "---", form, "---", change
        finally:
            obj.save()

    def resolve_param(self, obj):
        param = obj.param
        if is_json(param):
            if isinstance(json.loads(param), dict):
                return format_html(format_dict(json.loads(param)))

        return ("%s : %s" % (obj.paramname, param))
    resolve_param.short_description = '参数列表'

def is_json(myjson):
    try:
        json.loads(myjson, encoding='utf-8')
    except ValueError:
        return False
    return True

def format_dict(mydict):
    print mydict, type(mydict)
    s = ''
    s = s + '<table border="1">'
    for key, value in mydict.items():
        s = s + '<tr>'
        if isinstance(value, dict):
            s = s + ('<td>%s</td><td>%s</td>' % (key, format_dict(value)))
            # print format(value)
        else:
            s = s + ('<td>%s</td><td>%s</td>' % (key, str(value)))
        s = s + '</tr>'
    s = s + '</table>'
    return s

def compare_dict(info, be, af):
    for key in be:
        if key not in af.keys():
            print "删除"
            info['delete'].append(key)
        elif be[key] != af[key]:
            print '', be[key], type(be[key])
            if isinstance(be[key], dict):
                print "&&&&&", be[key], af[key]
                compare_dict(info, be[key], af[key])
                is_add(info, be[key], af[key])
            else:
                info['edit'].append((key, be[key], af[key]))

def is_add(info, be, af):
    for key in af:
        if key not in be.keys():
            print "新增"
            info['add'].append(key)

def edit_history(history, record):
    print "!!!!!!!!!!!", history
    h = {}
    if not history:
        h['record'] = []
    else:
        h = json.loads(history)
    h['record'].append(record)
    return json.dumps(h)

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
            if is_json(info[1]) and is_json(info[2]):
                s = s + '修改字段' + json.dumps(info[0]) + '从' + str(info[1]) + '到' + str(info[2]) + ','
            else:
                s = s + '修改字段' + json.dumps(info[0]) + '从' + json.dumps(info[1]) + '到' + json.dumps(info[2]) + ','
        s = s[:-1]
        return s



admin.site.register(Contact, ContactAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Tag, TagAdmin)