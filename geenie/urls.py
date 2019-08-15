from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('appbox/', v.appbox, name='appbox'),
    path('sharemarket/', v.sharemarket, name='sharemarket'),
    path('develop/', v.develop, name='develop'),
    path('mypage/', v.mypage, name='mypage'),
]
