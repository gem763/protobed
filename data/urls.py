from django.urls import path
from . import views as v

urlpatterns = [
    # path('', v.intro, name='intro'),
    path('newsinsight/', v.newsinsight, name='newsinsight'),
    path('update_newscloud/', v.update_newscloud, name='update_newscloud'),
    path('news/', v.news, name='news'),
]
