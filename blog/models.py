from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField

class Topic(models.Model):
    # topic 모델
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True)

class Post(models.Model):
    # 게시물 모델
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    content = RichTextUploadingField(blank=False, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    view = models.PositiveIntegerField(default=0)
    storage = models.CharField(max_length=1, default='Y')
    
