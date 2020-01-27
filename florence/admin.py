from django.contrib import admin
from florence.models import User, Module, Import, ModuleImport, UrlImport
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
admin.site.register(Import)
admin.site.register(ModuleImport)
admin.site.register(UrlImport)
# admin.site.register(Module)


class ImportInline(admin.TabularInline):
    model = Import

class ModuleAdmin(admin.ModelAdmin):
    inlines = [
        ImportInline,
    ]

admin.site.register(Module, ModuleAdmin)
