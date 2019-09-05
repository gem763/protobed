from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from data.models import Newsdata
from collections import Counter
import json
import pandas as pd
import time

# Create your views here.

def newsinsight(request):
    now = pd.Timestamp.utcnow()
    _from = (now - pd.DateOffset(days=1)).date()
    news = Newsdata.objects.filter(published_at__date__gte=_from).order_by('-downloaded_at')[:50]
    return render(request, 'data/newsinsight.html', {'news':news})


def news(request):
    if request.method=='GET':
        publisher = request.GET.get('publisher', None)
        date_from = request.GET.get('from', None)
        date_to = request.GET.get('to', None)
        news = Newsdata.objects.filter(publish_date__date__gte=date_from, publish_date__date__lte=date_to, publisher=publisher).order_by('-publish_date')
        news = list(news.values('publisher', 'title', 'publish_date', 'text', 'authors', 'url'))
        # print(news)
        return JsonResponse(news, safe=False)


def update_newscloud(request):
    if request.method=='GET':
        pub = request.GET.get('pub', None)
        days = request.GET.get('days', 3)

        now = pd.Timestamp.utcnow()
        # now = pd.Timestamp(Newsdata.objects.order_by('publish_date').last().publish_date)
        _from = (now - pd.DateOffset(days=days)).date()
        news = Newsdata.objects.filter(published_at__date__gte=_from)

        if pub is None:
            pass
            # news = news.order_by('-publish_date')[:50]

        else:
            pub = pub.split(',')
            news = news.filter(pub__in=pub)#.order_by('-publish_date')[:50]


        words = news.values_list('words', flat=True)

        s = time.time()
        counter = Counter()
        [counter.update(item) for item in words]
        # [counter.update(json.loads(item)) for item in words]
        # words = [item for sublist in words for item in json.loads(sublist)]
        # words = sum(list(words), [])
        # words = ','.join(words).split(',')
        print('22222222222222222222', time.time()-s); s = time.time()
        # words = (','.join([ws.lower() for ws in words])).split(',')
        # words = dict(Counter(words).most_common(100))
        words = dict(counter.most_common(100))
        # words.pop('me', None)
        print('333333333333333333333', time.time()-s); s = time.time()
        return JsonResponse(words, safe=False)


    # _hashtags = Hashtag.objects.filter(feed__timestamp__date__gte=_from).exclude(feed__content__contains='카지노').values_list('hashtag', flat=True)
