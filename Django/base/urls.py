from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),

    path('dashboard', views.menu, name='menu'),
    path('view', views.get_courses, name='view'),
    path('view/<int:pk>', views.get_course, name='view_course'),
    path('create', views.add_course, name='create'),
    path('update/<int:pk>', views.update_course, name='update'),
    path('delete/<int:pk>', views.delete_course, name='delete'),
]
