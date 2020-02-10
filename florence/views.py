from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from florence.models import User, Lib, Intlib
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from florence.serializers import IntlibSearchSerializer
import json

# Create your views here.

def intro(request):
    return render(request, 'florence/intro.html')

def dashboard(request):
    return render(request, 'florence/dashboard.html')

def miniapps(request):
    return render(request, 'florence/miniapps.html')

def develop(request):
    return render(request, 'florence/develop.html')

def my(request):
    return render(request, 'florence/my.html')

# def getcode(request):
#     modulekey = request.GET.get('modulekey', None)
#
#     try:
#         _modulekey = modulekey.split(':')
#         user_email = _modulekey[1]
#         module_name = _modulekey[2]
#         print(user_email, module_name)
#         module = Module.objects.get(author__email=user_email, name=module_name)
#         return JsonResponse({'success':True, 'code':module.code}, safe=False)
#
#     except:
#         return JsonResponse({'success':False}, safe=False)


# def treefy(mod):
#     imports = {}
#     for imp in mod.import_set.all():
#         if imp.typeof=='moduleimport':
#             imports[imp.alias] = treefy(imp.moduleimport.module)
#         elif imp.typeof=='urlimport':
#             imports[imp.alias] = imp.urlimport.url
#
#     return {
#         'imports': imports,
#         'code': mod.code,
#         'author': mod.author.email,
#         'author_avatar': mod.author.socialaccount_set.all()[0].get_avatar_url(),
#         'name': mod.name,
#         'description': mod.description,
#         'exports': [exp.strip() for exp in mod.exports.split(',')]
#     }
#
#
# def moduletree(request, pk):
#     mod = Module.objects.get(pk=pk)
#     return JsonResponse({'success':True, 'tree':treefy(mod)}, safe=False)
#
#
# def import_module(request, pk, alias):
#     mod = Module.objects.get(pk=pk)
#     mod.alias = alias
#     return render(request, 'florence/import_module.html', {'module':mod})


def familize(intlib):
    imports = {}
    for imp in intlib.imports.all():
        if imp.lib.typeof=='intlib':
            imports[imp.alias] = familize(imp.lib.intlib)
        elif imp.lib.typeof=='extlib':
            imports[imp.alias] = imp.lib.extlib.url

    return {
        'id': intlib.pk,
        'imports': imports,
        'code': intlib.code,
        'author': {
            'id': intlib.author.pk,
            'avatar': intlib.author.socialaccount_set.all()[0].get_avatar_url(),
        },
        'name': intlib.name,
        'description': intlib.description,
        'exports': [exp.strip() for exp in intlib.exports.split(',')]
    }


def lib_family(request, pk):
    lib = Intlib.objects.get(pk=pk)
    # ser = serializers.serialize('python', [lib], use_natural_foreign_keys=True)

    # print(JSONRenderer().render(IntlibSerializer(Intlib.objects.all(), many=True).data))
    return JsonResponse({'family':familize(lib)}, safe=False)


def lib_saerch(request):
    n = 3
    q = request.GET.get('q', None)

    try:
        vector = SearchVector('code', 'description', 'keywords')
        query = SearchQuery(q)
        searched = Intlib.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')[:n]
        result = IntlibSearchSerializer(searched, many=True).data
        # result = JSONRenderer().render(result)
        # result = list(searched.values('name', 'author_avatar', 'description', 'version'))
        # result = list(searched.values('name', 'author__avatar', 'description', 'version'))
        return JsonResponse({'result':result}, safe=False)

    except:
        return JsonResponse({'result':[]}, safe=False)
