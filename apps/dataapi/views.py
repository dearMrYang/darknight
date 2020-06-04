from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

# Create your views here.
from django.views import View

from apps.postoperate.models import Post, Category, Tags, Comments
from apps.userauth.models import User
from utils.localtime import SwitchDateTime
from utils.resultful import ResultCode


class GetPostList(View):
    """
    api获取文章数据
    """

    def get(self, request, *args, **kwargs):
        # 获取查询数据关键词
        search = request.GET.get('s', '')
        cid = int(request.GET.get('cid', 0))
        tid = int(request.GET.get('tid', 0))
        timerange = request.GET.get('timerange', '')
        # 查询关键词字典
        self.search_dict = {}
        self.search_dict['search'] = search
        self.search_dict['cid'] = cid
        self.search_dict['tid'] = tid
        self.search_dict['timerange'] = timerange
        # 返回的查询数据关键词
        res_query = {}
        # 数据分页与以及格式操作
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', settings.LIMIT))
        db_data = Post.objects.select_related('puser', 'pcategory').prefetch_related('ptags')
        db_data = self.search_post(db_data, res_query)
        paginator = Paginator(db_data, limit)
        paginator_data = self.paginator_page(paginator, page)
        data = self.format_res_data(paginator_data)

        # 返回数据总格式
        res_data = {
            "count": paginator.count,
            "data": data,
            "query": res_query if res_query else None,
        }
        return ResultCode.ok(**res_data)

    def paginator_page(self, paginator, page):
        """
        获取分页数据
        :param paginator:
        :param page:
        :return:
        """
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            # 页码错误， 返回第一页
            paginator_data = paginator.page(1)
        except EmptyPage:
            # 当前页没有数据（最后一页+1），获取最大页数据
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data

    def search_post(self, posts, query):
        """
        搜索数据
        :param posts:
        :param query:
        :return:
        """
        if self.search_dict['search']:  # 搜索
            query['s'] = self.search_dict['search']
            posts = posts.filter(ptitle__contains=self.search_dict['search'])
        if self.search_dict['cid']:  # 分类
            query['cid'] = self.search_dict['cid']
            posts = posts.filter(pcategory_id=self.search_dict['cid'])
        if self.search_dict['tid']:  # 标签
            query['tid'] = self.search_dict['tid']
            tid = Tags.objects.filter(id=self.search_dict['tid']).first()
            posts = posts.filter(ptags=tid)
        if self.search_dict['timerange']:  # 时间范围
            query['timerange'] = self.search_dict['timerange']
            posts = posts.filter(update_time__range=SwitchDateTime.time_range(self.search_dict['timerange']))
        return posts

    def format_res_data(self, paginator_data):
        """
        格式化返回数据
        :param paginator_data:
        :return:
        """
        data = []
        for item in paginator_data.object_list:
            data.append(dict(
                pid=item.pid,
                ptitle=item.ptitle,
                pthumbnail=item.pthumbnail,
                puser=item.puser.username if item.puser else '',
                update_time=SwitchDateTime.format_datetime(item.update_time),
                pcategory=item.pcategory.cname,
                ptags=[tag.tname for tag in item.ptags.all()],
            ))
        return data


class GetCategoryList(View):
    """
    api获取分类数据
    """

    def get(self, request):
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', settings.LIMIT))
        db_data = Category.objects.prefetch_related('posts').annotate(pnums=Count('posts'))
        paginator = Paginator(db_data, limit)
        paginator_data = self.paginator_page(paginator, page)

        data = self.format_res_data(paginator_data)

        # 返回数据总格式
        res_data = {
            "count": paginator.count,
            "data": data,
        }
        return ResultCode.ok(**res_data)

    def paginator_page(self, paginator, page):
        """
        获取分页数据
        :param paginator:
        :param page:
        :return:
        """
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            # 页码错误， 返回第一页
            paginator_data = paginator.page(1)
        except EmptyPage:
            # 当前页没有数据（最后一页+1），获取最大页数据
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data

    def format_res_data(self, paginator_data):
        """
        格式化返回数据
        """
        data = []
        for item in paginator_data:
            data.append(dict(
                id=item.id,
                name=item.cname,
                pnums=item.pnums,
                update_time=SwitchDateTime.format_datetime(item.update_time),
            ))
        return data


class GetTagsList(View):
    """
    api获取分类数据
    """

    def get(self, request):
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', settings.LIMIT))
        db_data = Tags.objects.prefetch_related('posts').annotate(pnums=Count('posts'))
        paginator = Paginator(db_data, limit)
        paginator_data = self.paginator_page(paginator, page)

        data = self.format_res_data(paginator_data)

        # 返回数据总格式
        res_data = {
            "count": paginator.count,
            "data": data,
        }
        return ResultCode.ok(**res_data)

    def paginator_page(self, paginator, page):
        """
        获取分页数据
        :param paginator:
        :param page:
        :return:
        """
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            # 页码错误， 返回第一页
            paginator_data = paginator.page(1)
        except EmptyPage:
            # 当前页没有数据（最后一页+1），获取最大页数据
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data

    def format_res_data(self, paginator_data):
        """
        格式化返回数据
        :param paginator_data:
        :return:
        """
        data = []
        for item in paginator_data:
            data.append(dict(
                id=item.id,
                name=item.tname,
                pnums=item.pnums,
                update_time=SwitchDateTime.format_datetime(item.update_time),
            ))
        return data


class GetCommentsList(View):
    """
    api获取分类数据
    """

    def get(self, request):
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', settings.LIMIT))
        pid = request.GET.get('pid', '')
        self.search_dict = {}
        self.search_dict['pid'] = pid
        db_data = Comments.objects.select_related('cpost').annotate(pnums=Count('cpost'))
        query = {}
        db_data = self.search_post(db_data, query)
        paginator = Paginator(db_data, limit)
        paginator_data = self.paginator_page(paginator, page)

        data = self.format_res_data(paginator_data)

        # 返回数据总格式
        res_data = {
            "count": paginator.count,
            "data": data,
        }
        return ResultCode.ok(**res_data)

    def search_post(self, posts, query):
        """
        搜索数据
        :param posts:
        :param query:
        :return:
        """
        if self.search_dict['pid']:  # 搜索
            query['pid'] = self.search_dict['pid']
            posts = posts.filter(cpost_id=self.search_dict['pid'])
        return posts

    def paginator_page(self, paginator, page):
        """
        获取分页数据
        :param paginator:
        :param page:
        :return:
        """
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            # 页码错误， 返回第一页
            paginator_data = paginator.page(1)
        except EmptyPage:
            # 当前页没有数据（最后一页+1），获取最大页数据
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data

    def format_res_data(self, paginator_data):
        """
        格式化返回数据
        :param paginator_data:
        :return:
        """
        data = []
        for item in paginator_data:
            data.append(dict(
                id=item.id,
                ccontent=item.ccontent,
                cuser=item.cuser.username,
                pid=item.cpost.pid,
                update_time=SwitchDateTime.format_datetime(item.update_time),
            ))
        return data


def home_data(request):
    """
    仪表板数据
    :param request:
    :return:
    """
    post_obj = Post.objects

    seven_day_value = []
    seven_day_name = []
    half_year_value = []
    half_year_name = []

    for date, date_range in zip(*SwitchDateTime.seven_day_date()):
        seven_day_name.insert(0, date)
        seven_day_value.insert(0, post_obj.filter(update_time__range=date_range).count())

    for date, date_range in zip(*SwitchDateTime.half_year_date()):
        half_year_name.insert(0, date)
        half_year_value.insert(0, post_obj.filter(update_time__range=date_range).count())

    data = {
        "seven_day_data": [seven_day_name, seven_day_value],
        "half_year_data": [half_year_name, half_year_value],
    }
    return ResultCode.ok(data=data)
