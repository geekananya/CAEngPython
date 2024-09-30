from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='root'),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('getposts', views.get_posts),
    path('createpost', views.add_post),
    path('deletepost/<int:pk>', views.delete_post),
]
