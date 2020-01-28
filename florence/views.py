from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from florence.models import Module, User

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
        'exports': [exp.strip() for exp in mod.exports.split(',')]
    }


def moduletree(requeset, pk):
    mod = Module.objects.get(pk=pk)
    # print(treefy(mod))
    return JsonResponse({'success':True, 'tree':treefy(mod)}, safe=False)


def import_module(request, pk, alias):
    mod = Module.objects.get(pk=pk)
    mod.alias = alias
    return render(request, 'florence/import_module.html', {'module':mod})
