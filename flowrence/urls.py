from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', v.dashboard, name='dashboard'),
    path('apphub/', v.apphub, name='apphub'),
    path('develop/', v.develop, name='develop'),
    path('my/', v.my, name='my'),
]
