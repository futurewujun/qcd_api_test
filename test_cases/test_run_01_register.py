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
import pytest

#读取到测试数据
register_data=DoExcel(project_path.case_path,'Register').read_data('RegisterCase')

@ddt    #修饰测试类
class RunCase(unittest.TestCase):
    def setUp(self):
        self.do_exl=DoExcel(project_path.case_path,'Register')    # 准备测试数据
        self.my_log=MyLog()
    # 登录注册
    @pytest.mark.moke_two
    @data(*register_data)   # 加*解包，相当于遍历test_data传入函数，与加unpack的区别是：加入了unpack后，date里有几个参数，下面的函数就要传入几个变量
    def test_case(self,case):
        global result   #声明全局变量
        method=case['Method']
        url=case['Url']
        param=eval(case['Params'])
        # print(param)

        expected=eval(case['ExpectedResult'])
        #发起测试
        # print('-------正在测试{}模块里面第{}条测试用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        self.my_log.info('正在执行{}模块第{}条用例：{}'.format(case['Module'],case['CaseId'],case['Title']))
        self.my_log.info('参数是：{}'.format(param))
        res=HttpRequest()  #实例化
        resp=res.http_request(method,url,param,cookies=None)
        print('实际结果：{}'.format(resp.json()))#http发送请求拿到的实际返回值
        #对比结果
        try:
            self.assertEqual(expected,resp.json())
            result='pass'
            self.my_log.info('该条测试用例通过')
            # print('该条测试用例通过')
        except  AssertionError as e:
            result='failed'
            self.my_log.error('该条测试用例不通过：'.format(e))
            # print('该条测试用例不通过:{}'.format(e))
        finally:
            final_result=result
            self.my_log.info('******开始写入数据******')
            self.do_exl.write_back(case['CaseId']+1,8,resp.text)   #写实际结果   #03：不同的表单写回，表单名就不能放在初始化函数中
            self.do_exl.write_back(case['CaseId']+1,9,final_result)    #写测试结果
            self.my_log.info('******写入数据完毕******')


if __name__ == '__main__':
    unittest.main()