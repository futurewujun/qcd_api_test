# -*- coding: utf-8 -*-
'''
脚本命令，pycharm里运行pytest
'''
import pytest

if __name__ == '__main__':
    # pytest.main(["-m moke_three"])   #
    pytest.main(["-m moke_two","-s","--alluredir=report/allure"])