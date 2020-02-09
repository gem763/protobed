from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', v.dashboard, name='dashboard'),
    path('miniapps/', v.miniapps, name='miniapps'),
    path('develop/', v.develop, name='develop'),
    # path('develop/getcode/', v.getcode, name='getcode'),
    path('module/<int:pk>/tree/', v.moduletree, name='moduletree'),
    path('module/<int:pk>/import/<str:alias>/', v.import_module, name='import_module'),

    # path('get_imported/', v.get_imported, name='get_imported'),

    path('my/', v.my, name='my'),
    path('lib/<int:pk>/family/', v.lib_family, name='lib_family'),
    path('lib/search/', v.lib_saerch, name='lib_search'),
]
