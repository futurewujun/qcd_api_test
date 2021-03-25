# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser
from common import project_path
class ReadConfig:

    def __init__(self):
        self.cf=ConfigParser()
        self.conf_path = project_path.conf_path
        self.cf.read(self.conf_path, encoding='utf-8')
        # 把配置文件所有数据全部读出来：
        self.db_config = self.get_str('DB','db_config')


        self.login_url = self.get_str('login','url')
        self.login_param = self.get_str('login','param')

    def get_data(self,section,option):
        '''从配置文件里面获取一个元组 字典 列表等类型的数据'''
        value=self.cf.get(section,option)#section  option
        return eval(value)
    def get_str(self,section,option):
        value=self.cf.get(section,option)
        return value

if __name__ == '__main__':
    res=ReadConfig().get_data('RechargeCase','case_id')
    print(res)
    print(type(res))
    print(ReadConfig().db_config)