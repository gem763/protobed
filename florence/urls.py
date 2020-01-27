from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', v.dashboard, name='dashboard'),
    path('miniapps/', v.miniapps, name='miniapps'),
    path('develop/', v.develop, name='develop'),
    path('develop/getcode/', v.getcode, name='getcode'),
    path('module/<int:pk>/tree/', v.moduletree, name='moduletree'), 

    path('my/', v.my, name='my'),
]
