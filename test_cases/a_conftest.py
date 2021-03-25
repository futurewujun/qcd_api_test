# -*- coding: utf-8 -*-

# import pytest
# from common.do_excel import DoExcel
# from common import project_path
# from common.log_test import MyLog
#
# @pytest.fixture(scope="function")
# # fixture 一般是放在conftest中
# def init_api():
#     '''获得初始值与测试数据'''
#     do_exl = DoExcel(project_path.case_path,"Login")
#     my_log = MyLog()
#     return do_exl,my_log   # 固定，每调用一次fixture，就取出一个数据,返回的是一个元祖
#     # yield request.param,do_exl,my_log     # yield 和return类似，返回函数的值，但函数遇到return自动终止，遇到yield要继续运行，
#                                             # 根据fixture的作用域来执行在函数退出，还是类，模块，会话()
#     # driver.quit()                     # 也就是要运行后面的，在web自动化中，执行完测试用例后可以退出浏览器