from django.urls import path

from . import views

app_name = 'sitecms'

urlpatterns = [
       path('', views.index, name='index'),


       path('home/', views.home, name='home'),

       path('post/list/', views.post_list, name='post_list'),
       path('post/write/', views.post_write, name='post_write'),
       path('category/list/', views.category_list, name='category_list'),
       path('tags/list/', views.tags_list, name='tags_list'),
       path('comments/list/', views.comments_list, name='comments_list'),
]
