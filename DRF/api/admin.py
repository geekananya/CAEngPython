from django.contrib import admin
from .models import Posts, PostsAdmin, UsersAdmin


# Register your models here.
admin.site.register(Posts, PostsAdmin)
# admin.site.register(Users, UsersAdmin)