# -*- coding: utf-8 -*-
# @Time    : 2020/5/2 15:18
# @Author  : dearMrYang
# @File    : localtime.py
# @Software: PyCharm
import datetime

from django.utils import timezone


class SwitchDateTime(object):
    """
    时间操作
    """

    @classmethod
    def __current_datetime(cls):
        """
        当前时间
        :return:
        """
        return timezone.now()

    @classmethod
    def format_datetime(cls, db_datetime):
        """
        格式化时间
        :param db_datetime:
        :return:
        """
        return db_datetime.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def format_date(cls, db_datetime):
        """
        格式化时间
        :param db_datetime:
        :return:
        """
        return db_datetime.strftime('%Y-%m-%d')

    @classmethod
    def half_year_date(cls):
        """
        获取前半年的时间
        :return:
        """
        current_datetime = cls.__current_datetime()
        half_year_date_list = []
        half_year_date_list_range = []
        for _ in range(6):
            # 当月第一天0：0
            month_first_day_min = datetime.datetime.combine(current_datetime.replace(day=1), datetime.time.min)
            current_month = month_first_day_min.month
            current_year = month_first_day_min.year
            if current_month == 12:
                current_year += 1
                current_month = 1
            else:
                current_month += 1
            # 当月最后一天23:59:59
            next_month = month_first_day_min.replace(current_year, current_month)
            month_last_day = next_month - datetime.timedelta(days=1)
            month_last_day_max = datetime.datetime.combine(month_last_day, datetime.time.max)

            half_year_date_list.append(month_first_day_min.strftime('%Y{year}%m{month}').format(year="年", month="月"))
            half_year_date_list_range.append([month_first_day_min, month_last_day_max])
            # 上月最后一天
            current_datetime = month_first_day_min - datetime.timedelta(days=1)
        return half_year_date_list, half_year_date_list_range

    @classmethod
    def seven_day_date(cls):
        """
        获取前七天的时间及其范围
        :return:
        """
        seven_day_date_list = []
        seven_day_date_list_range = []
        current_datetime = cls.__current_datetime()
        for _ in range(6):
            current_datetime_min = datetime.datetime.combine(current_datetime, datetime.time.min)
            current_datetime_max = datetime.datetime.combine(current_datetime, datetime.time.max)
            seven_day_date_list.append(current_datetime.strftime('%m{month}%d{day}').format(month="月", day="日"))
            seven_day_date_list_range.append([current_datetime_min, current_datetime_max])
            current_datetime -= datetime.timedelta(days=1)
        return seven_day_date_list, seven_day_date_list_range

    @classmethod
    def split_datetime(cls, db_datetime):
        """
        分离年月、月日
        :param db_datetime:
        :return:
        """
        return db_datetime.strftime('%Y-%m'), db_datetime.strftime('%m-%d')

    @classmethod
    def time_range(cls, time_range):
        """
        时间范围：start - （end + 1）
        :param time_range:
        :return:
        """
        start, end = time_range.split('+~+')
        return [datetime.datetime.strptime(start, '%Y-%m-%d'), datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)]
