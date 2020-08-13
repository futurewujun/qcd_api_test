# -*- coding: utf-8 -*-
from configparser import ConfigParser
from common import project_path
class ReadConfig:

    def __init__(self,file_name):
        self.cf=ConfigParser()
        self.cf.read(file_name,encoding='utf-8')

    def get_data(self,section,option):
        '''从配置文件里面获取一个元组 字典 列表等类型的数据'''
        value=self.cf.get(section,option)#section  option
        return eval(value)
    def get_str(self,section,option):
        value=self.cf.get(section,option)
        return value

if __name__ == '__main__':
    res=ReadConfig(project_path.conf_path).get_data('RechargeCase','case_id')
    print(res)
    print(type(res))
