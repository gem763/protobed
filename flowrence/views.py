from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def intro(request):
    return render(request, 'flowrence/intro.html')

def dashboard(request):
    return render(request, 'flowrence/dashboard.html')

def apphub(request):
    return render(request, 'flowrence/apphub.html')

def develop(request):
    return render(request, 'flowrence/develop.html')

def my(request):
    return render(request, 'flowrence/my.html')
