from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    picture = models.ImageField(upload_to="profile-avatar", default='profile-avatar/default_user.png')

    firstname = models.CharField(max_length=42,default="Anonymous", blank=True)
    lastname = models.CharField(max_length=42,default="Anonymous", blank=True)
    #username = models.CharField(max_length=50)
    #gender = models.CharField(max_length=200, null = True)
    location = models.CharField(max_length=42, default="", blank=True)
    cellphone = models.CharField(max_length=42, default="", blank=True)

    def __unicode__(self):
        return self.user.username
    @staticmethod
    def get_userinfos(user):
        return UserInfo.objects.filter(user=user)



class Comment(models.Model):
    comment = models.CharField(max_length=42, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.from_user.username+":"+self.comment

class Job(models.Model):
    title = models.CharField(max_length=100, blank=False)
    content = models.CharField(max_length=1000, blank=False)
    user = models.ForeignKey(User, related_name="who_write")
    date_created = models.DateTimeField(auto_now_add=True)
    locationState = models.CharField(max_length=200, blank=False, default = "USA")
    picture = models.ImageField(upload_to="post-photos", blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null = True)
    commentsNum = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment,related_name='job_comments', null=True)
    hasNewComment = models.BooleanField(default=False)
    def __unicode__(self):
        return self.content

