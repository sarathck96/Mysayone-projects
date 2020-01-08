from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError



class Sayoneuser(models.Model):
    name = models.CharField(max_length=70, validators=[MinLengthValidator(5)])
    mailid = models.EmailField(max_length=70)
    username = models.CharField(max_length=70)
    password = models.CharField(max_length=30)
    cnf_pass = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='images')
    user = models.OneToOneField(User, related_name='sayone_user', on_delete=models.CASCADE)

class Story(models.Model):
    story_type_choices = (
        (0,"Event"),
        (1,"Blog"),
        (2,"Image Gallery"),
    )
    story_id = models.AutoField(primary_key=True)
    story_title = models.CharField(max_length=50)
    story_type = models.IntegerField(choices=story_type_choices,default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    story_user = models.ForeignKey(User,related_name='story_user',on_delete=models.CASCADE)

class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    blog_pic = models.ImageField(upload_to='images')
    blog_description = models.CharField(max_length=200)
    story = models.ForeignKey(Story,on_delete=models.CASCADE,related_name='blog_story')



