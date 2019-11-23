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
from common import get_data
from common.do_re import Do_re
import pytest


#读取到测试数据
login_data = DoExcel(project_path.case_path,'Login').read_data('LoginCase')
# 正则替换    TODO:全部替换
p = '#(.*?)#'
login_data_new = eval(Do_re().do_re(p,str(login_data)))
# TODO 传测试用例数据的方式之一：直接传入parametrize中自动解包,用parametrize后面的用例类就要加个参数接收，如下面的case
@pytest.fixture(scope="function")
# TODO fixture 一般是放在conftest中，只能是conftest；在外面 每个测试用例执行时会自动发现conftest的fixture，会先运行conftest里的
# 不用在测试用例中导入conftest
def init_api(request):
    '''获得初始值与测试数据'''
    do_exl = DoExcel(project_path.case_path,"Login")
    my_log = MyLog()
    return do_exl,my_log   # 固定，每调用一次fixture，就取出一个数据,返回的是一个元祖
    # yield request.param,do_exl,my_log     # yield 和return类似，返回函数的值，但函数遇到return自动终止，遇到yield要继续运行，
                                            # 根据fixture的作用域来执行在函数退出，还是类，模块，会话()
    # driver.quit()                     # 也就是要运行后面的，在web自动化中，执行完测试用例后可以退出浏览器

# @ddt    #修饰测试类
# TODO 在类前面也可以使用fixture，引入conftest的init_api
# @pytest.mark.usefixtures("init_api")
class TestCase:
    # 登录注册
    # @pytest.mark.moke
    @pytest.mark.parametrize('case',login_data_new)  # TODO 相当于ddt,case要与下面测试用例函数的参数一致
    # @data(*login_data)   # 加*解包，相当于遍历test_data传入函数，与加unpack的区别是：加入了unpack后，date里有几个参数，下面的函数就要传入几个变量
    def test_case(self,case,init_api):
        '''case 是上面传的测试用例数据'''
        do_exl = init_api[0]
        my_log = init_api[1]

        global result   #声明全局变量
        method=case['Method']
        url=case['Url']
        param=eval(case['Params'])
        # print(param)
        expected=eval(case['ExpectedResult'])

        # 调用正则函数替换mobilephone,pwd：TODO:只替换Params
        param=eval(get_data.replace(case['Params']))

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
        finally:
            final_result=result
            my_log.info('******开始写入数据******')
            do_exl.write_back(case['CaseId']+1,8,resp.text)   #写实际结果   #03：不同的表单写回，表单名就不能放在初始化函数中
            do_exl.write_back(case['CaseId']+1,9,final_result)    #写测试结果
            my_log.info('******写入数据完毕******')
if __name__ == '__main__':
    # pytest.main(["-m moke"])
    pytest.main(['-s'])