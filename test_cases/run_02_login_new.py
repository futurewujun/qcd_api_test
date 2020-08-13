# -*- coding: utf-8 -*-
import unittest
from ddt import ddt,data
from common.do_excel import DoExcel
from common.project_path import case_path
from common.http_request import HttpRequest
from common.log_test import MyLog
from common.do_re import Do_re
# from API_Pr ogram.API_06.common.read_config import ReadConfig

login_data = DoExcel(case_path,'Login').read_data('LoginCase')
# 正则替换    TODO:全部替换
p = '#(.*?)#'
login_data_new = eval(Do_re().do_re(p,str(login_data)))
# print(login_data_new)
# print(type(login_data_new))
@ddt
class RunCase(unittest.TestCase):
    def setUp(self):
        self.do_exl = DoExcel(case_path,'Login')
        self.my_log = MyLog()
    @data(*login_data_new)  #测试数据
    def test_case(self,case): #传入测试数据整体
        global result
        method = case['Method']
        url = case['Url']
        param = eval(case['Params'])    # params 本身是一个字符串
        expected_result = eval(case['ExpectedResult'])  # 本身也是一个字符串
    # 发起测试
        self.my_log.info('正在执行{}模块第{}条用例：{}'.format(case['Module'], case['CaseId'], case['Title']))
        self.my_log.info('参数是{}'.format(param))
    #     实例化请求
        res = HttpRequest()
        resp = res.http_request(method,url,param,cookies=None)
        print('实际结果是{}'.format(resp.json()))
    #   对比
        try:
            self.assertEqual(expected_result,resp.json())
            result = 'pass'
            self.my_log.info('该条用例通过')
        except Exception as e:
            result = 'failed'
            self.my_log.info('该条用例失败,{}'.format(e))
            raise e
        finally:
            final_result = result
            # 写会实际结果与是否通过
            self.do_exl.write_back(case['CaseId']+1,8,resp.text)    # TODO:注意是写回text，不能写回json
            self.do_exl.write_back(case['CaseId']+1,9,final_result)
            self.my_log.info('写入数据完毕')
        self.my_log.info('本条用例结束')



    def tearDown(self):
        pass
