from django.http import HttpResponse
from django.urls import path

from .views import *

app_name = 'dataapi'

urlpatterns = [
    path('posts/getlist/', GetPostList.as_view(), name='post_list'),
    path('category/getlist/', GetCategoryList.as_view(), name='category_list'),
    path('tags/getlist/', GetTagsList.as_view(), name='tags_list'),
    path('comments/getlist/', GetCommentsList.as_view(), name='comments_list'),
    path('home/data/', home_data, name='home_data'),

]
