from django.db import models
from custom_user.models import AbstractEmailUser

# Create your models here.


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractEmailUser, BigIdAbstract):
    credit = models.IntegerField(default=0)

    def __str__(self):
        return self.email



class Module(BigIdAbstract):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)
    nlike = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    keywords = models.TextField(max_length=500, null=True, blank=True)
    published = models.BooleanField(default=False)
    code = models.TextField(null=False, blank=False)
    exports = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        disp = self.name + ' | ' + self.author.email

        if self.published:
            return '[published] ' + disp

        else:
            return disp


class Import(BigIdAbstract):
    on = models.ForeignKey(Module, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, blank=True, null=True)

    def cast(self):
        for subclass in self.__class__.__subclasses__():
            try:
                return getattr(self, subclass.__name__.lower())
            except:
                pass

        return self

    @property
    def typeof(self):
        return self.cast().__class__.__name__.lower()

    def __str__(self):
        return str(self.on) + ' | ' + self.alias

class ModuleImport(Import):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class UrlImport(Import):
    url = models.URLField(max_length=300, blank=False, null=False)
