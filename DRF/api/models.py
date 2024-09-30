from django.db import models
from django.contrib import admin


# Create your models here.

class Posts(models.Model):
    author_id = models.IntegerField()
    body = models.TextField()
    tags = models.CharField(null=True, blank=True, max_length=100) # list of tags separated by space
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class PostsAdmin(admin.ModelAdmin):        # change the django admin model display
    list_display = ('id', 'author_id', 'body', 'tags', 'likes','created_at')
    fields = ('author_id', 'body', 'tags', 'likes')

#
# class Users(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)


class UsersAdmin(admin.ModelAdmin):        # change the django admin model display
    list_display = ('id', 'name', 'email')
    fields = ('name', 'email')