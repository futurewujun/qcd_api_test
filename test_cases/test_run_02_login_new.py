# -*- coding: utf-8 -*-
import unittest
from ddt import ddt,data
from common.do_excel import DoExcel
from common.project_path import case_path
from common.http_request import HttpRequest
from common.log_test import MyLog
from common.do_re import Do_re
# from API_Pr ogram.API_06.common.read_config import ReadConfig
import pytest
import requests


login_data = DoExcel(case_path,'Login').read_data('LoginCase')
# 正则替换    TODO:全部替换
p = '#(.*?)#'
login_data_new = eval(Do_re().do_re(p,str(login_data)))

# 默认是function级别的，这里设置为class级别
# TODO  传测试用例数据的方式之二：通过fixture的params传入，再return request.parm，后面通过定义的函数返回的元祖序列号去取值
# @pytest.fixture(params=login_data_new)
# def ready_go(request):
#     '''获得初始值与测试数据'''
#     do_exl = DoExcel(case_path,"Login")
#     my_log = MyLog()
#     return request.param,do_exl,my_log   # 固定，每调用一次fixture，就取出一个数据,返回的是一个元祖

@pytest.mark.moke
def test_case(init_api): #传入测试数据整体
    global result
    method = init_api[0]['Method']
    url = init_api[0]['Url']
    param = eval(init_api[0]['Params'])    # params 本身是一个字符串
    expected_result = eval(init_api[0]['ExpectedResult'])  # 本身也是一个字符串
# 发起测试
    init_api[2].info('正在执行{}模块第{}条用例：{}'.format(init_api[0]['Module'], init_api[0]['CaseId'], init_api[0]['Title']))
    init_api[2].info('参数是{}'.format(param))
    #    实例化请求
    res = HttpRequest()
    resp = res.http_request(method,url,param,cookies=None)
    print('实际结果是{}'.format(resp.json()))
    #  对比
    try:
        assert expected_result == resp.json()
        result = 'pass'
        init_api[2].info('该条用例通过')
    except Exception as e:
        result = 'failed'
        init_api[2].info('该条用例失败,{}'.format(e))
        raise e

    MyLog().info('本条用例结束')
if __name__ == '__main__':
    pytest.main(["-m moke_three"])

