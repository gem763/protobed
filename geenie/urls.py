from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('appbox/', v.appbox, name='appbox'),
]
