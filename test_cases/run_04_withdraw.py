# -*- coding: utf-8 -*-
# 1：引入单元测试
# 2：引入ddt
# 3：测试用例里面引入引入try...except..finally，并写回测试结果
# 4：引入日志
# 5：完成用例的可配置化：想跑哪条用例，就在配置文件里面写好
# 6：搞定全局变量（path变量，数据与文件分离）
import unittest
from ddt import ddt,data

from common.do_excel import DoExcel
from common.http_request import HttpRequest
from common import project_path
from common.log_test import MyLog
from common.get_data import GetData
from common import get_data
'''根据反射取值cookies'''

#读取到测试数据
withdraw_data=DoExcel(project_path.case_path,'Withdraw').read_data('WithdrawCase')

@ddt    #修饰测试类
class RunCase(unittest.TestCase):
    def setUp(self):
        self.do_exl=DoExcel(project_path.case_path,'Withdraw')    # 准备测试数据
        self.my_log=MyLog()

    @data(*withdraw_data)   # 加*解包，相当于遍历test_data传入函数，与加unpack的区别是：加入了unpack后，date里有几个参数，下面的函数就要传入几个变量
    def test_case2(self,case_2):
        global result1
        # url_login='http://47.107.168.87:8080/futureloan/mvc/api/member/login'
        # param_login={'mobilephone':'18688775656','pwd':'123456'}
        # method_login='get'
        # # 获取到登录的cookies
        # cookies=HttpRequest().http_request(method_login,url_login,param_login,cookies=None).cookies
        url=case_2['Url']
        param=eval(case_2['Params'])
        method=case_2['Method']
        expected=eval(case_2['ExpectedResult'])

        # if case_2['Params'].find('normal_phone') != -1:
        #     param['mobilephone']=getattr(GetData,'normal_phone')

        # 调用正则函数替换mobilephone，pwd：
        param=eval(get_data.replace(case_2['Params']))
        # print(param)

        self.my_log.info('正在执行{}模块第{}条用例：{}'.format(case_2['Module'],case_2['CaseId'],case_2['Title']))
        self.my_log.info('参数是：{}'.format(param))

        resp=HttpRequest().http_request(method,url,param,cookies=getattr(GetData,'cookies')) #根据反射取值cookies
        print('实际结果是：{}'.format(resp.json()))   #发起请求的实际结果
        if resp.cookies:    #为真，即存在cookies
            setattr(GetData,'cookies',resp.cookies) #根据反射重新赋值cookies

        # 对比结果
        try:
            self.assertEqual(expected['code'],resp.json()['code'])  #对比code
            result1='pass'
            self.my_log.info('该条测试用例通过')
        except AssertionError as e:
            self.my_log.error('该条测试用例不通过：{}'.format(e))
            result1='failed'
        finally:
            final_result=result1
            self.my_log.info('******开始写入数据******')
            self.do_exl.write_back(case_2['CaseId']+1,8,resp.text)
            self.do_exl.write_back(case_2['CaseId']+1,9,final_result)
            self.my_log.info('******写入数据完毕******')

