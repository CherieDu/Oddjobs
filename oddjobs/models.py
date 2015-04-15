from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to="profile-avatar", default='profile-avatar/default_user.png')

    def __unicode__(self):
        return self.user.username
    @staticmethod
    def get_userinfos(user):
        return UserInfo.objects.filter(user=user)
