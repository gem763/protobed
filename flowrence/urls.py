from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('dashboard/', v.dashboard, name='dashboard'),
    path('publica/', v.publica, name='publica'),
    path('develop/', v.develop, name='develop'),
    path('my/', v.my, name='my'),
]
