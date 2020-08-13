# -*- coding: utf-8 -*-
from common.get_data import GetData
import re
class Do_re:
    '''正则匹配'''
    def __init__(self):
        '''正则匹配要传的三个初始值
        :param pattern   正则表达式
        :param value     替换的值
        :param target    需要的替换的目标字符串

        '''
        # self.pattern = pattern
        # self.value = value
        # self.target = target
    def do_re(self,p,target):
        while re.search(p,target):
            resp = re.search(p,target)
            key = resp.group(1)
            # print(key)
            res_val = getattr(GetData,key)
            # print(res_val)
            # TODO：sub 是返回一个新的字符串，要赋值回去，赋值给原来的值，才是‘替换’成功
            target = re.sub(p,res_val,target,count=1)
            # print(re.sub(p,res_val,target,count=1))
        return target
if __name__ == '__main__':
    p = '#(.*?)#'
    target = "{'mobilephone':'#normal_phone#','pwd':'#normal_pwd#'}"
    print(Do_re().do_re(p,target))
