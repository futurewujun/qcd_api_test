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
@pytest.fixture(params=login_data_new)
def ready_go(request):
    '''获得初始值与测试数据'''
    do_exl = DoExcel(case_path,"Login")
    my_log = MyLog()
    return request.param,do_exl,my_log   # 固定，每调用一次fixture，就取出一个数据,返回的是一个元祖

@pytest.mark.moke
def test_case(ready_go): #传入测试数据整体
    global result
    method = ready_go[0]['Method']
    url = ready_go[0]['Url']
    param = eval(ready_go[0]['Params'])    # params 本身是一个字符串
    expected_result = eval(ready_go[0]['ExpectedResult'])  # 本身也是一个字符串
# 发起测试
    ready_go[2].info('正在执行{}模块第{}条用例：{}'.format(ready_go[0]['Module'], ready_go[0]['CaseId'], ready_go[0]['Title']))
    ready_go[2].info('参数是{}'.format(param))
    #    实例化请求
    res = HttpRequest()
    resp = res.http_request(method,url,param,cookies=None)
    print('实际结果是{}'.format(resp.json()))
    #  对比
    try:
        assert expected_result == resp.json()
        result = 'pass'
        ready_go[2].info('该条用例通过')
    except Exception as e:
        result = 'failed'
        ready_go[2].info('该条用例失败,{}'.format(e))
        raise e
    finally:
        final_result = result
        # 写会实际结果与是否通过
        ready_go[1].write_back(ready_go[0]['CaseId']+1,8,resp.text)    # TODO:注意是写回text，不能写回json
        ready_go[1].write_back(ready_go[0]['CaseId']+1,9,final_result)
        ready_go[2].info('写入数据完毕')
    MyLog().info('本条用例结束')
if __name__ == '__main__':
    pytest.main(["-m moke_three"])

