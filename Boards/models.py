from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def get_total_topics(self):
        return Topic.objects.filter(board=self).count()

    def get_total_posts(self):
        return Post.objects.filter(topic__board=self).count() - Topic.objects.filter(board=self).count()

    def get_last_topic(self):
        return Topic.objects.filter(board=self).latest("updated_at")

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, null=True, related_name='topics', on_delete=models.SET_NULL)
    views_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, editable=False)

    def get_last_post(self):
        return Post.objects.filter(topic=self).latest("created_at")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length=3000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        topic = self.topic
        topic.updated_at = timezone.now()
        topic.save()
        return super().save(*args, **kwargs)

    