from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.BigAutoField(help_text="User ID", primary_key=True)
    user_name = models.CharField(max_length=100)

class Post(models.Model):
    post_id = models.BigAutoField(help_text="Post ID", primary_key=True)
    post_title = models.CharField(max_length=200)
    content = models.TextField(blank=False, null=False)
    post_writer = models.ForeignKey("User")
    post_create = models.DateTimeField(auto_now_add=True)
    post_update = models.DateTimeField(auto_now=True)
    post_topic = models.CharField(max_length=200)
    post_view = models.PositiveIntegerField(default=0)
    
class Topic(models.Model):
    topic_id = models.BigAutoField(help_text="Topic ID", primary_key=True)
    topic_name = models.CharField(max_length=100)
