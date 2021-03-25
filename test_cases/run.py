# -*- coding: utf-8 -*-
# 1：引入单元测试
# 2：引入ddt
# 3：测试用例里面引入引入try...except..finally，并写回测试结果
# 4：引入日志
# 5：完成用例的可配置化：想跑哪条用例，就在配置文件里面写好
# 6：搞定全局变量（path变量，数据与文件分离）

# import unittest
# import sys
# sys.path.append('./')   #把根目录追加到sys.path
# print(sys.path) #python编译的路径
import os

import pytest
# from common import project_path
# from test_cases import test_run_01_register #具体到模块
# from test_cases import test_run_02_login
# from test_cases import test_all
# from test_cases import run_04_withdraw
# import os
# # 进程池：
# from multiprocessing import Pool
# def run0():
#     os.system("pytest -v --tb=short test_all.p::test_register --allure .././result")
# def run1():
#     os.system("pytest -v --tb=short test_all.py::test_login")
# def run2():
#     os.system("pytest -v --tb=short test_all.py::test_recharge")
# def run3():
#     os.system("pytest -v --tb=short test_all.py::test_withraw")


# if __name__ == '__main__':
    # print('-' * 20)
    #
    # # 设置最大进程池4个，并发数最多4
    # pool = Pool(4)
    # pool.apply_async(run0(),)
    # pool.apply_async(run1(),)
    # pool.apply_async(run2(),)
    # pool.apply_async(run3(),)
    #
    # # 关闭进程池
    # pool.close()
    #
    # # 阻塞进程，否则一个进程运行结束，主进程就结束了，其他未结束正在运行的进程也会被强制结束
    # pool.join()
    # print('-'*20)

pytest.main(['-s','--alluredir','../../report/result','test_all.py'])
# os.system('')