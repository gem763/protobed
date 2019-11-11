from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def intro(request):
    return render(request, 'flowrence/intro.html')

def dashboard(request):
    return HttpResponse('dashboard')

def publica(request):
    return HttpResponse('publica')

def develop(request):
    return HttpResponse('develop')

def my(request):
    return HttpResponse('my')
