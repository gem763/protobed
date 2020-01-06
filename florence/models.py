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
    # imports = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        disp = self.name + ' | ' + self.author.email

        if self.published:
            return '[published] ' + disp

        else:
            return disp
