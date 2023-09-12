from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    # topic 모델
    name = models.CharField(max_length=100)

class Post(models.Model):
    # 게시물 모델
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL)
    view = models.PositiveIntegerField(default=0)
    

