# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 21:18
# @Author  : dearMrYang
# @File    : resultful.py
# @Software: PyCharm
from django.http import JsonResponse


class ResultCode(object):
    """
    成功 ==> 0
    参数错误 ==> 1
    没权限 ==> 200
    方法错误 ==> 400
    服务器错误 ==> 500
    """
    ok_code = 0
    params_error_code = 1
    auth_error_code = 200
    method_error_code = 400
    serve_error_code = 500

    @classmethod
    def _result_method(cls, code, msg=None, data=None, count=None, **kwargs):
        """
        Ajax请求返回JSON
        :param code:
            状态码
        :param msg:
            信息
        :param data:
            数据
        :param kwargs:
        :return:
        """
        _result = dict(
            code=code,
            msg=msg,
            count=count,
            data=data,
        )
        if kwargs and isinstance(kwargs, dict) and kwargs.keys():
            _result.update(kwargs)
        return JsonResponse(_result)

    @classmethod
    def ok(cls, msg="成功~", data=None, count=None, **kwargs):
        return cls._result_method(cls.ok_code, msg=msg, data=data, count=count, **kwargs)

    @classmethod
    def params_error(cls, msg="参数错误~", data=None, count=None, **kwargs):
        return cls._result_method(cls.params_error_code, msg=msg, data=data, count=count, **kwargs)

    @classmethod
    def auth_error(cls, msg="权限错误~", data=None, count=None, **kwargs):
        return cls._result_method(cls.auth_error_code, msg=msg, data=data, count=count, **kwargs)

    @classmethod
    def method_error(cls, msg="方法错误~", data=None, count=None, **kwargs):
        return cls._result_method(cls.method_error_code, msg=msg, data=data, count=count, **kwargs)

    @classmethod
    def serve_error(cls, msg="服务器错误~", data=None, count=None, **kwargs):
        return cls._result_method(cls.serve_error_code, msg=msg, data=data, count=count, **kwargs)
