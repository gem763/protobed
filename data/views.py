from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from data.models import Newsdata
from collections import Counter
import json
import pandas as pd

# Create your views here.

def newscloud(request):
    return render(request, 'data/newscloud.html')


def update_newscloud(request):
    if request.method=='GET':
        publisher = request.GET.get('publisher', None)
        days = request.GET.get('days', 20)

        now = pd.Timestamp(Newsdata.objects.order_by('publish_date').last().publish_date)
        _from = (now - pd.DateOffset(days=days)).date()
        news = Newsdata.objects.filter(publish_date__date__gte=_from)

        if publisher is None:
            pass
            # news = news.order_by('-publish_date')[:50]

        else:
            publisher = publisher.split(',')
            news = news.filter(publisher__in=publisher)#.order_by('-publish_date')[:50]

        words = news.values_list('words', flat=True)
        words = sum([ws.lower().split(',') for ws in words], [])
        words = dict(Counter(words).most_common(100))
        words.pop('he', None)
        words.pop('who', None)
        words.pop('what', None)
        words.pop('it', None)
        words.pop('we', None)
        words.pop('you', None)
        words.pop('him', None)
        words.pop('i', None)
        words.pop('her', None)
        words.pop('she', None)
        words.pop('they', None)
        words.pop('them', None)
        words.pop('me', None)
        return JsonResponse(words, safe=False)


    _hashtags = Hashtag.objects.filter(feed__timestamp__date__gte=_from).exclude(feed__content__contains='카지노').values_list('hashtag', flat=True)
