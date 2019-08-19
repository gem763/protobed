from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from data.models import Newsdata
from collections import Counter

# Create your views here.

def newscloud(request):
    if request.method=='GET':
        publisher = request.GET.get('publisher', None)

        if publisher is None:
            news = Newsdata.objects.all().order_by('-publish_date')[:50]

        else:
            publisher = publisher.split(',')
            news = Newsdata.objects.filter(publisher__in=publisher).order_by('-publish_date')[:50]

        words = news.values_list('words', flat=True)
        words = sum([ws.split(',') for ws in words], [])
        words = dict(Counter(words).most_common(100))
        return render(request, 'data/newscloud.html', {'words':words})
