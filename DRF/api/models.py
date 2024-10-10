from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Posts(models.Model):
    # author_id = models.IntegerField()
    author_username = models.CharField(max_length=20)
    body = models.TextField()
    tags = models.CharField(default="", blank=True, max_length=100) # list of tags separated by space
    likes_no = models.IntegerField(default=0)      # possibly store usernames of liked separated by space
    created_at = models.DateTimeField(auto_now_add=True)


class PostsAdmin(admin.ModelAdmin):        # change the django admin model display
    list_display = ('id', 'author_username', 'body', 'tags', 'likes_no','created_at')
    fields = ('author_username', 'body', 'tags', 'likes')

#
# class Users(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)


class UsersAdmin(admin.ModelAdmin):        # change the django admin model display
    list_display = ('id', 'name', 'email')
    fields = ('name', 'email')


class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')  # composite pk

    def __str__(self):
        return f'Post ID: {self.post.id}, User ID: {self.user.id}'