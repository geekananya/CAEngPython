from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='root'),
    path('auth/login', views.login),
    path('auth/register', views.register),
    path('auth/logout', views.logout),
    # superuser only
    path('auth/getusers', views.get_users),
    path('auth/deleteuser/<int:pk>', views.delete_user),

    path('posts/get/', views.get_posts),
    path('posts/get/<int:pk>', views.get_post),
    path('posts/get/<str:tag>', views.search_post_by_tag),
    path('posts/create', views.add_post),
    path('posts/update/<int:pk>', views.update_post),
    path('posts/delete/<int:pk>', views.delete_post),
    path('posts/like/<int:pk>', views.like_post),
    path('posts/unlike/<int:pk>', views.unlike_post),
    path('posts/getlikes/', views.get_likes),
    path('posts/getlikestatus/<int:pk>', views.get_like_status),
]
