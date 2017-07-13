# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from blog import models
from django.shortcuts import render

# Create your views here.
from blog.models import BlogsPost
from django.shortcuts import render_to_response

def index(request):
    blog_list = models.BlogsPost.objects.all()
    return render_to_response('blog_index.html',{'blog_list':blog_list})