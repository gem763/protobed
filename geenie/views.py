from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def intro(request):
    return render(request, 'geenie/intro.html')


def appbox(request):
    return render(request, 'geenie/appbox.html')
