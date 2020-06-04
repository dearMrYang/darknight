import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from apps.postoperate.models import Category, Tags, Post, Comments
from apps.userauth.models import User
from utils.resultful import ResultCode

"""
/operate/category/add/
/operate/category/edit/
/operate/category/delete/

/operate/tags/add/
/operate/tags/edit/
/operate/tags/delete/


/operate/post/write/
/operate/post/delete/
"""


@csrf_exempt
@require_POST
def post_write(request):
    """
    发布文章
    :param request:
        title: 标题
        desc: 描述
        content: 内容
        category_id: 分类id
        tags_list: 标签id list
        thumbnail: 封面
    :return:
    """
    title = request.POST.get('title')
    desc = request.POST.get('desc')
    content = request.POST.get('content')
    category_id = request.POST.get('category')
    tags_list = request.POST.getlist('tags[]')
    thumbnail = request.POST.get('thumbnail')
    if not all([title, desc, content, category_id, thumbnail]):
        return ResultCode.params_error(msg="还有必填项未填写~")
    db_category = Category.objects.filter(id=int(category_id))
    post = Post.objects.create(
        ptitle=title,
        pdesc=desc,
        pcontent=content,
        pcategory=db_category.first(),
        pthumbnail=thumbnail,
        puser=User.objects.first(),
    )
    for item in tags_list:
        if not item:
            continue
        db_tag = Tags.objects.filter(id=int(item))
        if db_tag.exists():
            post.ptags.add(db_tag.first())
            post.save()
    return ResultCode.ok()


@require_GET
def post_delete(request):
    """
    删除文章
    :param request:
       id: 需要删除的分类id string||list
    :return:
    """

    def delete(id):
        """
        删除数据
        :param id:
        :return:
        """
        if not id:
            return ResultCode.params_error()
        db_post_by_id = Post.objects.filter(pid=id)
        if not db_post_by_id.exists():
            return ResultCode.params_error(msg="该文章不存在~")
        # 模拟删除
        db_post_by_id.update(is_del=True)
        # 删除数据
        # db_post_by_id.delete()

    pid = request.GET.get('pid')
    pids = request.GET.getlist('pid[]')
    if pids:
        for item in pids:
            delete(item)
    else:
        delete(pid)
    return ResultCode.ok()


@csrf_exempt
@require_POST
def category_add(request):
    """
    添加新分类
    :param request:
        name: 新分类名
    :return:
    """
    name = request.POST.get('name', '').lower()
    if not name:
        return ResultCode.params_error()
    db_category = Category.objects.filter(cname=name)
    if db_category.exists():
        return ResultCode.params_error(msg="该分类已存在~")
    name = Category.objects.create(cname=name)
    return ResultCode.ok()


@csrf_exempt
@require_POST
def category_edit(request):
    """
    修改分类
    :param request:
        id: 需要修改的分类id
        name: 新分类名
    :return:
    """
    id = int(request.POST.get('id', 0))
    name = request.POST.get('name', '').lower()
    if not all([id, name]):
        return ResultCode.params_error()
    db_category_by_id = Category.objects.filter(id=int(id))
    if not db_category_by_id.exists():
        return ResultCode.params_error(msg="该分类不存在~")
    db_category_by_name = Category.objects.filter(cname=name)
    if db_category_by_name.exists():
        return ResultCode.params_error(msg="该分类已存在~")
    name = db_category_by_id.update(cname=name)
    return ResultCode.ok()


@require_GET
def category_delete(request):
    """
    删除分类
    :param request:
        id: 需要删除的分类id
    :return:
    """

    def delete(id):
        if not id:
            return ResultCode.params_error()
        db_category_by_id = Category.objects.filter(id=int(id))
        if not db_category_by_id.exists():
            return ResultCode.params_error(msg="该分类不存在~")
        # 模拟删除
        db_category_by_id.update(is_del=True)
        # 删除数据
        # db_category_by_id.delete()

    id = request.GET.get('id')
    ids = request.GET.getlist('id[]')
    if ids:
        for item in ids:
            delete(item)
    else:
        delete(id)
    return ResultCode.ok()


@csrf_exempt
@require_POST
def tags_add(request):
    """
    添加新标签
    :param request:
        name: 新标签名
    :return:
    """
    name = request.POST.get('name', '').lower()
    if not name:
        return ResultCode.params_error()
    db_tag = Tags.objects.filter(tname=name)
    if db_tag.exists():
        return ResultCode.params_error(msg="该标签已存在~")
    name = Tags.objects.create(tname=name)
    return ResultCode.ok()


@csrf_exempt
@require_POST
def tags_edit(request):
    """
    修改标签
    :param request:
        id: 需要修改的标签id
        name: 新标签名
    :return:
    """
    id = int(request.POST.get('id', 0))
    name = request.POST.get('name', '').lower()
    if not all([id, name]):
        return ResultCode.params_error()
    db_tag_by_id = Tags.objects.filter(id=int(id))
    if not db_tag_by_id.exists():
        return ResultCode.params_error(msg="该标签不存在~")
    db_tag_by_name = Tags.objects.filter(tname=name)
    if db_tag_by_name.exists():
        return ResultCode.params_error(msg="该标签已存在~")
    name = db_tag_by_id.update(tname=name)
    return ResultCode.ok()


@require_GET
def tags_delete(request):
    """
    删除标签
    :param request:
        id: 需要删除的标签id
    :return:
    """

    def delete(id):
        if not id:
            return ResultCode.params_error()
        db_tag_by_id = Tags.objects.filter(id=int(id))
        if not db_tag_by_id.exists():
            return ResultCode.params_error(msg="该标签不存在~")
        # 模拟删除
        db_tag_by_id.update(is_del=True)
        # 删除数据
        # db_tag_by_id.delete()

    id = request.GET.get('id')
    ids = request.GET.getlist('id[]')
    if ids:
        for id in ids:
            delete(id)
    else:
        delete(id)
    return ResultCode.ok()


@require_GET
def comments_delete(request):
    """
    删除标签
    :param request:
        id: 需要删除的评论id
    :return:
    """

    def delete(id):
        if not id:
            return ResultCode.params_error()
        db_tag_by_id = Comments.objects.filter(id=int(id))
        if not db_tag_by_id.exists():
            return ResultCode.params_error(msg="该评论不存在~")
        # 模拟删除
        db_tag_by_id.update(is_del=True)
        # 删除数据
        # db_tag_by_id.delete()

    id = request.GET.get('id')
    ids = request.GET.getlist('id[]')
    if ids:
        for id in ids:
            delete(id)
    else:
        delete(id)
    return ResultCode.ok()


"""
# 上传图片
"""


@csrf_exempt
@require_POST
def upload_file(request):
    """
    上传图片
    :param request:
    :return:
    """
    flag = False
    if request.GET.get('guid', ''):
        flag = True
        file = request.FILES.get('editormd-image-file')
    else:
        file = request.FILES.get('file')
    try:
        ext = file.name.split('.')[-1]
    except:
        return JsonResponse(data={
            "success": 0,  # 0 表示上传失败，1 表示上传成功
            "message": "上传错误~~",
            "url": ''  # 上传成功时才返回
        })
    name = uuid.uuid4().hex + '.' + ext
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    pathname = settings.MEDIA_URL + name
    url = request.build_absolute_uri(pathname)
    if flag:
        return JsonResponse(data={
            "success": 1,  # 0 表示上传失败，1 表示上传成功
            "message": "提示的信息",
            "url": url  # 上传成功时才返回
        })
    return ResultCode.ok(msg="上传成功！", data={
        "name": name,
        "url": url,
        "pathname": pathname
    })
