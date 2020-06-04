from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from apps.postoperate.models import Category, Tags, Comments, Post
from apps.userauth.models import User


@login_required
def index(request):
    return render(request, 'backend/index.html')


def home(request):
    post_nums = Post.objects.filter(is_del=False).count()
    category_nums = Category.objects.filter(is_del=False).count()
    comment_nums = Comments.objects.filter(is_del=False).count()
    tags_nums = Tags.objects.filter(is_del=False).count()
    user_nums = User.objects.filter(is_del=False).count()
    context = {
        "post_nums": post_nums,
        "category_nums": category_nums,
        "comment_nums": comment_nums,
        "user_nums": user_nums,
        "tags_nums": tags_nums,
    }
    return render(request, 'backend/home.html', context=context)


def post_list(request):
    categories = Category.objects.values('id', 'cname')
    tags = Tags.objects.values('id', 'tname')
    context = {
        "categories": categories,
        "tags": tags,
    }
    return render(request, 'backend/page/post-list.html', context=context)


def post_write(request):
    categories = Category.objects.values('id', 'cname')
    tags = Tags.objects.values('id', 'tname')
    context = {
        "categories": categories,
        "tags": tags,
    }
    return render(request, 'backend/page/post-write.html', context=context)


def category_list(request):
    return render(request, 'backend/page/category-list.html')


def tags_list(request):
    return render(request, 'backend/page/tag-list.html')


def comments_list(request):
    posts = Post.objects.values('pid', 'ptitle')
    context = {
        'posts': posts
    }
    return render(request, 'backend/page/comment-list.html', context=context)
