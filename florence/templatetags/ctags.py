from django import template
from florence.models import Module
register = template.Library()

# @register.filter
# def of_name(namepair):
#     return Brand.objects.filter(name__in=namepair)


# @register.filter
# def of_name2(bname):
#     return Brand.objects.get(name=bname)
