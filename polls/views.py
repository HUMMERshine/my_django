# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import HttpResponse

from django.shortcuts import render

# Create your views here.
def index(request):
    #return HttpResponse("hello world!")
    #return render(request, "index.html")
    if request.method == 'POST':
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        print "*****"
        print (username, password)
    return render(request, "index.html")
