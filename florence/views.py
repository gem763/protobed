from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from florence.models import Module, User
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

def getcode(request):
    modulekey = request.GET.get('modulekey', None)

    try:
        _modulekey = modulekey.split(':')
        user_email = _modulekey[1]
        module_name = _modulekey[2]
        print(user_email, module_name)
        module = Module.objects.get(author__email=user_email, name=module_name)
        return JsonResponse({'success':True, 'code':module.code}, safe=False)

    except:
        return JsonResponse({'success':False}, safe=False)


def treefy(mod):
    imports = {}
    for imp in mod.import_set.all():
        if imp.typeof=='moduleimport':
            imports[imp.alias] = treefy(imp.moduleimport.module)
        elif imp.typeof=='urlimport':
            imports[imp.alias] = imp.urlimport.url

    return {
        'imports': imports,
        'code': mod.code,
        'author': mod.author.email,
        'author_avatar': mod.author.socialaccount_set.all()[0].get_avatar_url(),
        'name': mod.name,
        'description': mod.description,
        'exports': [exp.strip() for exp in mod.exports.split(',')]
    }


def moduletree(request, pk):
    mod = Module.objects.get(pk=pk)
    return JsonResponse({'success':True, 'tree':treefy(mod)}, safe=False)


def import_module(request, pk, alias):
    mod = Module.objects.get(pk=pk)
    mod.alias = alias
    return render(request, 'florence/import_module.html', {'module':mod})


def get_imported(request):
    # module_id = request.POST.get('module_id', None)
    # url = request.POST.get('url', None)
    #alias = request.POST.get('alias', None)
    imported = json.loads(request.POST.get('imported', None))
    # print(imported)
    #
    # if (module is not None) and (url is None):
    #     imported = Module.objects.get(pk=module_id)
    #     imported.type = 'module'
    #
    # elif (module is None) and (url is not None):
    #     imported.type = 'url'
    #
    # imported.alias = alias
    return render(request, 'florence/imported.html', {'imported':imported})
