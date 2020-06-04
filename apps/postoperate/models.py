from django.db import models

# Create your models here.
from apps.baseModel import BaseModel
from shortuuidfield import ShortUUIDField

from apps.userauth.models import User


class Category(BaseModel):
    cname = models.CharField(verbose_name='分类名', max_length=10)

    class Meta:
        ordering = ['-update_time']
        db_table = 'db_category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tags(BaseModel):
    tname = models.CharField(verbose_name='标签名', max_length=10)

    class Meta:
        ordering = ['-update_time']
        db_table = 'db_tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Post(BaseModel):
    pid = ShortUUIDField(primary_key=True)
    ptitle = models.CharField(verbose_name='标题', max_length=30)
    pdesc = models.CharField(verbose_name='描述', max_length=300)
    pthumbnail = models.URLField(verbose_name='封面图')
    pcontent = models.TextField(verbose_name='内容')

    puser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pcategory = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    ptags = models.ManyToManyField(Tags, blank=True, related_name='posts')

    class Meta:
        ordering = ['-update_time']
        db_table = 'db_post'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    # 下一篇
    def next_post(self):
        # [5-6, 5-5, 5-4]  下一篇取最后
        posts = Post.objects.filter(update_time__gt=self.update_time)
        return posts.last() if posts else []

    # 上一篇
    def pre_post(self):
        # [5-2, 5-1, 4-30] 上一篇取第一
        posts = Post.objects.filter(update_time__lt=self.update_time)
        return posts.first() if posts else []


class Comments(BaseModel):
    ccontent = models.TextField()
    cuser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cpost = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time']
        db_table = 'db_comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
