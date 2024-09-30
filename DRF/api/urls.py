from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='root'),
    path('auth/login', views.login),
    path('auth/register', views.register),
    path('auth/logout', views.logout),

    path('posts/get', views.get_posts),
    path('posts/get/<int:pk>', views.get_post),
    path('posts/create', views.add_post),
    path('posts/update/<int:pk>', views.update_post),
    path('posts/delete/<int:pk>', views.delete_post),
    path('posts/like/<int:pk>', views.like_post),
    path('posts/search/<str:tag>', views.search_post_by_tag),
]
