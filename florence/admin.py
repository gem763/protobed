from django.contrib import admin
from florence.models import User, Lib, LocalLib, CdnLib, Module#, Import
from florence.models import Import2#, ModuleImport, UrlImport
from custom_user.admin import EmailUserAdmin
# Register your models here.


# class CustomEmailUserAdmin(EmailUserAdmin):
#     """
#     You can customize the interface of your model here.
#     """
#     pass


# admin.site.register(CustomEmailUser)
# admin.site.register(CustomEmailUser, CustomEmailUserAdmin)
admin.site.register(User)
admin.site.register(Lib)
admin.site.register(LocalLib)
admin.site.register(CdnLib)
# admin.site.register(Import)

admin.site.register(Import2)
# admin.site.register(ModuleImport)
# admin.site.register(UrlImport)


# class ImportInline(admin.TabularInline):
#     model = Import2
#
# class ModuleAdmin(admin.ModelAdmin):
#     inlines = [
#         ImportInline,
#     ]
#
# admin.site.register(Module, ModuleAdmin)
