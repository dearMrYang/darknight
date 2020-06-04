from django.conf import settings
from django.db.models import Count, F
from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.postoperate.models import Post, Category, Tags
from utils.localtime import SwitchDateTime


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def page_err(request):
    return render(request, '404.html', status=500)


def base_context(c_side=True, t_side=True):
    """
    侧边数据
    :return:
    """
    new_posts = Post.objects.values('pid', 'ptitle', 'pdesc', 'update_time')
    categories = Category.objects.select_related('posts'). \
        annotate(pnums=Count('posts'), name=F('cname')). \
        values('id', 'name', 'pnums').order_by('-pnums')
    tags = Tags.objects.prefetch_related('posts'). \
        annotate(pnums=Count('posts'), name=F('tname')). \
        values('id', 'name', 'pnums').order_by('-pnums')
    return {
        "new_posts": new_posts[0:settings.FRONT_NEW_POST_LIMIT],
        "categories": categories[0:settings.FRONT_CATEGORY_LIMIT] if c_side else categories,
        "tags": tags[0:settings.FRONT_TAGS_LIMIT] if t_side else tags,
        "c_side": c_side,
        "t_side": t_side,
    }


def get_pagination_data(paginator, page_obj, around_count=2):
    current_page = page_obj.number
    num_pages = paginator.num_pages

    left_has_more = False
    right_has_more = False
    # 左边的页数小于 around_count + 2 个就不显示省略号
    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)

    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)

    return {
        # left_pages：代表的是当前这页的左边的页的页码
        'left_pages': left_pages,
        # right_pages：代表的是当前这页的右边的页的页码
        'right_pages': right_pages,
        'current_page': current_page,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'num_pages': num_pages
    }


def index(request):
    page = int(request.GET.get('p', 1))
    s = request.GET.get('s', '')
    db_posts = Post.objects.filter(is_del=False, ptitle__contains=s). \
        values('pid', 'ptitle', 'pthumbnail', 'pdesc', 'update_time')
    paginator = Paginator(db_posts, settings.FRONT_LIMIT)
    try:
        posts_data = paginator.page(page)
    except PageNotAnInteger:
        # 页码错误， 返回第一页
        posts_data = paginator.page(1)
    except EmptyPage:
        # 当前页没有数据（最后一页+1），获取最大页数据
        posts_data = paginator.page(paginator.num_pages)
    pagination_data = get_pagination_data(paginator, posts_data)
    context = {
        "posts_data": posts_data,
        "url_query": "" if not s else "&s=" + s,
        "s": s
    }
    context.update(pagination_data)
    context.update(base_context())
    return render(request, 'front/index.html', context=context)


def detail(request, pid):
    post = Post.objects.select_related('pcategory').prefetch_related('puser', 'ptags').filter(pid=pid)
    if not post.exists():
        raise Http404()
    post = post.first()
    pre_post = post.pre_post()
    next_post = post.next_post()
    tags = Tags.objects.filter(posts__pid=pid)
    context = {
        'post': post,
        'tags': tags,
        'next_post': next_post,
        'pre_post': pre_post,
    }
    return render(request, 'front/detail.html', context=context)


def category(request):
    page = int(request.GET.get('p', 1))
    cid = int(request.GET.get('cid', 0))
    if cid:
        db_posts = Post.objects.filter(is_del=False, pcategory_id=cid). \
            values('pid', 'ptitle', 'pthumbnail', 'pdesc', 'update_time')
    else:
        db_posts = Post.objects.filter(is_del=False). \
            values('pid', 'ptitle', 'pthumbnail', 'pdesc', 'update_time')
    paginator = Paginator(db_posts, settings.FRONT_LIMIT)
    try:
        posts_data = paginator.page(page)
    except PageNotAnInteger:
        # 页码错误， 返回第一页
        posts_data = paginator.page(1)
    except EmptyPage:
        # 当前页没有数据（最后一页+1），获取最大页数据
        posts_data = paginator.page(paginator.num_pages)
    pagination_data = get_pagination_data(paginator, posts_data)
    context = {
        "posts_data": posts_data,
        "url_query": "" if not cid else "&cid=" + str(cid),
        "cid": cid,
    }
    context.update(pagination_data)
    context.update(base_context(c_side=False))
    return render(request, 'front/tags.html', context=context)


def tags(request):
    page = int(request.GET.get('p', 1))
    tid = int(request.GET.get('tid', 0))
    if tid:
        db_tag = Tags.objects.filter(id=tid)
        if not db_tag.exists():
            raise Http404()
        db_posts = Post.objects.filter(is_del=False, ptags=db_tag.first()). \
            values('pid', 'ptitle', 'pthumbnail', 'pdesc', 'update_time')
    else:
        db_posts = Post.objects.filter(is_del=False). \
            values('pid', 'ptitle', 'pthumbnail', 'pdesc', 'update_time')
    paginator = Paginator(db_posts, settings.FRONT_LIMIT)
    try:
        posts_data = paginator.page(page)
    except PageNotAnInteger:
        # 页码错误， 返回第一页
        posts_data = paginator.page(1)
    except EmptyPage:
        # 当前页没有数据（最后一页+1），获取最大页数据
        posts_data = paginator.page(paginator.num_pages)
    pagination_data = get_pagination_data(paginator, posts_data)
    context = {
        "posts_data": posts_data,
        "url_query": "" if not tid else "&tid=" + str(tid),
        "tid": tid,
    }
    context.update(pagination_data)
    context.update(base_context(t_side=False))
    return render(request, 'front/tags.html', context=context)


def archive(request):
    posts = Post.objects. \
        values('pid', 'ptitle', 'update_time'). \
        filter(is_del=False)
    posts_data = []
    date_flag = []
    for item in posts:
        date_year_month, date_month_day = SwitchDateTime.split_datetime(item.pop('update_time'))
        # 创建字典日期
        if date_year_month not in date_flag:
            date_flag.append(date_year_month)
            data_date_dict = {}
            data_date_dict[date_year_month] = []
            posts_data.append(data_date_dict)
        # 添加该日期数据
        data_date_dict[date_year_month].append(dict(
            pid=item.pop('pid'),
            ptitle=item.pop('ptitle'),
            update_time=date_month_day,
        ))
    context = {
        "posts_data": posts_data,
    }
    context.update(base_context())
    return render(request, 'front/archive.html', context=context)
