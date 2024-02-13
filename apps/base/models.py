from collections.abc import Iterable
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.authentication.models import User
from . import validator


class File(models.Model):
    file = models.FileField(blank=True, null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    def __str__(self):
        return f"File Uploaded for id: {self.id}"


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_hidden = models.BooleanField(default=False)
    hide_from = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='hide_post')

    def __str__(self):
        return str(self.user.firstname) + " " + str(self.user.lastname) + " post"


class Comment(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='comment')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post')
    text = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"`{self.user.firstname} {self.user.lastname}` ------- {self.post.user.firstname} {self.post.user.lastname}ning postiga comment yozdi"

class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='like')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)
    date_liked = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural ="Likes"
        
    def __str__(self):
        return "%s %s %sga like bosdi" % (self.user.firstname, self.user.lastname, self.post)
