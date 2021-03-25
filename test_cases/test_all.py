# -*- coding: utf-8 -*-
# 1：引入单元测试
# 2：引入ddt
# 3：测试用例里面引入引入try...except..finally，并写回测试结果
# 4：引入日志
# 5：完成用例的可配置化：想跑哪条用例，就在配置文件里面写好
# 6：搞定全局变量（path变量，数据与文件分离）
import os
import unittest
from ddt import ddt,data
import json
from common.do_excel import DoExcel
from common.http_request import HttpRequest
from common import project_path
from common.log_test import MyLog
from common.do_sql import DoSql
from common.get_data import GetData,replace
from common import do_re
import allure
import pytest
#读取到测试数据
register_data = DoExcel(project_path.case_path,'Register').read_data('RegisterCase')
login_data = DoExcel(project_path.case_path,'Login').read_data('LoginCase')
p = '#(.*?)#'
login_data_new = eval(do_re.Do_re().do_re(p,str(login_data)))
recharge_data = DoExcel(project_path.case_path,'Recharge').read_data('RechargeCase')
withdraw_data = DoExcel(project_path.case_path,'Withdraw').read_data('WithdrawCase')
Addloan_data = DoExcel(project_path.case_path,'Addloan').read_data('AddloanCase')
Invest_data = DoExcel(project_path.case_path,'Invest').read_data('InvestCase')


cookies=None    #先定义cookies=None

'''定义全局变量cookies解决'''

class TestCase:

    @pytest.mark.parametrize('case',register_data)
    @allure.feature("登录模块")
    @allure.title("登录")
    def test_register(self,case,init_api):
        my_log = init_api
        global result   #声明全局变量
        method=case['Method']
        url=case['Url']
        param=eval(case['Params'])
        # print(param)

        expected=eval(case['ExpectedResult'])
        #发起测试
        # print('-------正在测试{}模块里面第{}条测试用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        my_log.info('正在执行{}模块第{}条用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        my_log.info('参数是：{}'.format(param))
        res=HttpRequest()  #实例化
        resp=res.http_request(method,url,param,cookies=None)
        print('实际结果：{}'.format(resp.json()))#http发送请求拿到的实际返回值
        #对比结果
        try:
            assert expected == resp.json()
            result='pass'
            my_log.info('该条测试用例通过')
            # print('该条测试用例通过')
        except  AssertionError as e:
            result='failed'
            my_log.error('该条测试用例不通过：'.format(e))
            # print('该条测试用例不通过:{}'.format(e))

    @pytest.mark.parametrize('case',login_data_new)  # TODO 相当于ddt,case要与下面测试用例函数的参数一致
    # @data(*login_data)   # 加*解包，相当于遍历test_data传入函数，与加unpack的区别是：加入了unpack后，date里有几个参数，下面的函数就要传入几个变量
    def test_login(self,case,init_api):
        '''case 是上面传的测试用例数据'''
        my_log = init_api
        global result   #声明全局变量
        method=case['Method']
        url=case['Url']
        param=eval(case['Params'])
        # print(param)
        expected=eval(case['ExpectedResult'])
        # 调用正则函数替换mobilephone,pwd：TODO:只替换Params
        param=eval(replace(case['Params']))
        #发起测试
        # print('-------正在测试{}模块里面第{}条测试用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        my_log.info('正在执行{}模块第{}条用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        my_log.info('参数是：{}'.format(param))
        res=HttpRequest()  #实例化
        resp=res.http_request(method,url,param,cookies=None)
        print('实际结果：{}'.format(resp.json()))#http发送请求拿到的实际返回值
        # print('测试',type(resp.json()['code']))
        #对比结果
        try:
            assert expected == resp.json()
            result='pass'
            my_log.info('该条测试用例通过')
            # print('该条测试用例通过')
        except  AssertionError as e:
            result='failed'
            my_log.error('该条测试用例不通过：'.format(e))
            # print('该条测试用例不通过:{}'.format(e))


    @pytest.mark.parametrize('case',recharge_data)
    def test_recharge(self,case,init_api):
        my_log = init_api
        global result1  #定义为全局变量
        global cookies
        url=case['Url']
        param=eval(case['Params'])
        method=case['Method']
        expected=eval(case['ExpectedResult'])
        # 调用正则函数替换mobilephone，pwd：
        param=eval(replace(case['Params']))

        my_log.info('正在执行{}模块第{}条用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        my_log.info('参数是：{}'.format(param))
        # 拿到请求之前的账户余额
        if case['Sql'] != None:
            sql=eval(case['Sql'])['sql']
            before_LeaveAmount=DoSql().do_sql(sql)[0]
        resp=HttpRequest().http_request(method,url,param,cookies=cookies) #执行请求
        print('实际结果是：{}'.format(resp.json()))   #发起请求的实际结果
        if resp.cookies:  # 为真，即存在cookies继续执行 --- 判断请求的cookies是否为空  ---- 其实就是判断第一个登陆用例的cookies（resp的cookies）
            cookies=resp.cookies    #将默认的cookies替换为 登陆的cookies
            # 对比结果
        try:
            # 拿到充值之后的账户余额
            if case['Sql'] != None:
                after_LeaveAmount=DoSql().do_sql(eval(case['Sql'])['sql'])[0]
                recharge_amount=param['amount']
                expected_amount=before_LeaveAmount + recharge_amount
                assert expected_amount == after_LeaveAmount
            if case['ExpectedResult'].find('expect_amount') > -1:    #判断是否替换leaveamount,存在就替换
                case['ExpectedResult']=case['ExpectedResult'].replace('expect_amount',str(expected_amount)) #要接收替换的字符串
                # print(case_2['ExpectedResult'])
            assert eval(case['ExpectedResult']) == resp.json()  #对比
            result1='pass'
            my_log.info('该条测试用例通过')
        except AssertionError as e:
            my_log.error('该条测试用例不通过：{}'.format(e))
            result1='failed'

    @pytest.mark.parametrize('case',withdraw_data)
    def test_withraw(self,case,init_api):
        my_log = init_api

        global result1
        url=case['Url']
        param=eval(case['Params'])
        method=case['Method']
        expected=eval(case['ExpectedResult'])

        # if case_2['Params'].find('normal_phone') != -1:
        #     param['mobilephone']=getattr(GetData,'normal_phone')

        # 调用正则函数替换mobilephone，pwd：
        param=eval(replace(case['Params']))
        # print(param)

        my_log.info('正在执行{}模块第{}条用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        my_log.info('参数是：{}'.format(param))

        resp=HttpRequest().http_request(method,url,param,cookies=getattr(GetData,'cookies')) #根据反射取值cookies
        print('实际结果是：{}'.format(resp.json()))   #发起请求的实际结果
        if resp.cookies:    #为真，即存在cookies
            setattr(GetData,'cookies',resp.cookies) #根据反射重新赋值cookies

        # 对比结果
        try:
            assert expected['code']==resp.json()['code']  #对比code
            result1='pass'
            my_log.info('该条测试用例通过')
        except AssertionError as e:
            my_log.error('该条测试用例不通过：{}'.format(e))
            result1='failed'
# 进程池：
from multiprocessing import Pool
def run0():
    os.system("pytest -vs --tb=short test_all.py::test_register")
def run1():
    os.system("pytest -vs --tb=short test_all.py::test_login")
def run2():
    os.system("pytest -vs --tb=short test_all.py::test_recharge")
def run3():
    os.system("pytest -vs --tb=short test_all.py::test_withraw")


if __name__ == '__main__':
    print('-' * 20)

    # 设置最大进程池4个，并发数最多4
    pool = Pool(4)
    pool.apply_async(run0(),)
    pool.apply_async(run1(),)
    pool.apply_async(run2(),)
    pool.apply_async(run3(),)

    # 关闭进程池
    pool.close()

    # 阻塞进程，否则一个进程运行结束，主进程就结束了，其他未结束正在运行的进程也会被强制结束
    pool.join()
    print('-'*20)