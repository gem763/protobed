from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from florence.models import Module, User

# Create your views here.

def intro(request):
    return render(request, 'florence/intro.html')

def dashboard(request):
    return render(request, 'florence/dashboard.html')

def miniapps(request):
    return render(request, 'florence/miniapps.html')

def develop(request):
    return render(request, 'florence/develop.html')

def my(request):
    return render(request, 'florence/my.html')

def module(request, pk):
    code = Module.objects.get(pk=pk).code
    return JsonResponse({'code':code}, safe=False)
