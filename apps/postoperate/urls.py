from django.urls import path
from . import views

app_name = 'operate'
urlpatterns = [
    path('category/add/', views.category_add, name='category_add'),
    path('category/edit/', views.category_edit, name='category_edit'),
    path('category/delete/', views.category_delete, name='category_delete'),
    path('tags/add/', views.tags_add, name='tags_add'),
    path('tags/edit/', views.tags_edit, name='tags_edit'),
    path('tags/delete/', views.tags_delete, name='tags_delete'),

    path('comments/delete/', views.comments_delete, name='comments_delete'),

    path('post/write/', views.post_write, name='post_write'),
    path('post/delete/', views.post_delete, name='post_delete'),

    path('upload_file/', views.upload_file, name='upload_file'),
]
