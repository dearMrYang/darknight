from django.urls import path, re_path

from . import views


app_name = 'front'
urlpatterns = [
       path('', views.index, name="index"),
       path('s/', views.index, name="search"),
       re_path('p/(?P<pid>[0-9a-zA-Z]{22})/', views.detail, name="detail"),
       path('category/', views.category, name="category"),
       path('tags/', views.tags, name="tags"),
       path('archive/', views.archive, name="archive"),
]




