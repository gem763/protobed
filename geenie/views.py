from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def intro(request):
    return render(request, 'geenie/intro.html')


def appbox(request):
    return render(request, 'geenie/appbox.html')


def sharemarket(request):
    return render(request, 'geenie/sharemarket.html')


def develop(request):
    return render(request, 'geenie/develop.html')


def mypage(request):
    return render(request, 'geenie/mypage.html')
