# -*- coding: utf-8 -*-
# 1：引入单元测试
# 2：引入ddt
# 3：测试用例里面引入引入try...except..finally，并写回测试结果
# 4：引入日志
# 5：完成用例的可配置化：想跑哪条用例，就在配置文件里面写好
# 6：搞定全局变量（path变量，数据与文件分离）
import unittest
from ddt import ddt,data
import json
from common.do_excel import DoExcel
from common.http_request import HttpRequest
from common import project_path
from common.log_test import MyLog
from common.do_sql import DoSql
from common import get_data

#读取到测试数据
recharge_data=DoExcel(project_path.case_path,'Recharge').read_data('RechargeCase')
cookies=None    #先定义cookies=None

'''定义全局变量cookies解决'''

@ddt    #修饰测试类
class RunCase(unittest.TestCase):
    def setUp(self):
        self.do_exl=DoExcel(project_path.case_path,'Recharge')    # 准备测试数据
        self.my_log=MyLog()

    @data(*recharge_data)
    def test_case2(self,case_2):
        global result1  #定义为全局变量
        global cookies
        url=case_2['Url']
        param=eval(case_2['Params'])
        method=case_2['Method']
        # print(case_2['ExpectedResult'])
        expected=eval(case_2['ExpectedResult'])
        # if case_2['Params'].find('normal_phone') != -1:
        #     param['mobilephone']=getattr(GetData,'normal_phone')

        # 调用正则函数替换mobilephone，pwd：
        param=eval(get_data.replace(case_2['Params']))

        self.my_log.info('正在执行{}模块第{}条用例：{}'.format(case_2['Module'],case_2['CaseId'],case_2['Title']))
        self.my_log.info('参数是：{}'.format(param))
        # 拿到请求之前的账户余额
        if case_2['Sql'] != None:
            sql=eval(case_2['Sql'])['sql']
            before_LeaveAmount=DoSql().do_sql(sql)[0]

        resp=HttpRequest().http_request(method,url,param,cookies=cookies) #执行请求
        print('实际结果是：{}'.format(resp.json()))   #发起请求的实际结果
        if resp.cookies:  # 为真，即存在cookies继续执行 --- 判断请求的cookies是否为空  ---- 其实就是判断第一个登陆用例的cookies（resp的cookies）
            cookies=resp.cookies    #将默认的cookies替换为 登陆的cookies
            # 对比结果
        try:
            # 拿到充值之后的账户余额
            if case_2['Sql'] != None:
                after_LeaveAmount=DoSql().do_sql(eval(case_2['Sql'])['sql'])[0]
                recharge_amount=param['amount']
                expected_amount=before_LeaveAmount + recharge_amount
                self.assertEqual(expected_amount,after_LeaveAmount)
            if case_2['ExpectedResult'].find('expect_amount') > -1:    #判断是否替换leaveamount,存在就替换
                case_2['ExpectedResult']=case_2['ExpectedResult'].replace('expect_amount',str(expected_amount)) #要接收替换的字符串
                # print(case_2['ExpectedResult'])

            self.assertEqual(eval(case_2['ExpectedResult']),resp.json())  #对比
            result1='pass'
            self.my_log.info('该条测试用例通过')
        except AssertionError as e:
            self.my_log.error('该条测试用例不通过：{}'.format(e))
            result1='failed'
        finally:
            final_result=result1
            self.my_log.info('******开始写入数据******')
            self.do_exl.write_back(case_2['CaseId']+1,9,resp.text)
            self.do_exl.write_back(case_2['CaseId']+1,10,final_result)
            self.my_log.info('******写入数据完毕******')

