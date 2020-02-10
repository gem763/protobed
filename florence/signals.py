from allauth.socialaccount.signals import social_account_updated
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
from florence.models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        instance.init_user()


# @receiver(social_account_updated)
# def allauth_social_account_updated(request, sociallogin, **kwargs):
#     # https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/models.py
#     # user_signed_up 이후 user_logged_in이 자동호출된다
#     # 따라서 user_logged_in에서 set_social_avatar()를 하면 해당 기능이 두번 실행된다
#     sociallogin.user.set_default_avatar()
#
#
# @receiver(user_signed_up)
# def allauth_user_signed_up(request, user, **kwargs):
#     avatar = user.set_default_avatar()
