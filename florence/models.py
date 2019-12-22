from django.db import models
from custom_user.models import AbstractEmailUser

# Create your models here.


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class CustomEmailUser(AbstractEmailUser, BigIdAbstract):
    pass


class Profile(BigIdAbstract):
    user = models.OneToOneField(CustomEmailUser, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)

    # def natural_key(self):
    #     return {'id':self.pk, 'image':self.user.socialaccount_set.all()[0].get_avatar_url(), 'email':self.user.email}


class ModuleDefault(BigIdAbstract):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)
    nlike = models.IntegerField(default=0)
    code = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    

    class Meta:
        abstract = True
