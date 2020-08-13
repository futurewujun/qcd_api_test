# -*- coding: utf-8 -*-
import re
from common.read_config import ReadConfig
from common import project_path

config=ReadConfig(project_path.conf_path)
# print(config)

class GetData:
    '''动态的更改、删除、获取 数据'''
    cookies=None    #属性
    LOANID=None
    normal_phone=config.get_str('Data','normal_phone')
    normal_pwd=config.get_str('Data','normal_pwd')
    normal_memberid=config.get_str('Data','normal_memberid')
    # normal_loan_id=config.get_str('Data','normal_loan_id')



'''使用正则，查找替换
   target:目标字符串'''
def replace(target):
    '''循环一次替换一个参数'''
    p = '#(.*?)#'
    while re.search(p,target):  #找到参数化的字符就返回一个 match object, 即True
        m=re.search(p,target)   #在字符串里根据正则表达式来查找，有匹配的就返回match object
        key=m.group(1)  #拿到key，填参数1是只取 需要的字符串，不包括符号
        # print(key)
        value=getattr(GetData,key)   #取到要替换的内容 TODO ;这里根据属性名得到属性值，所以要保证用例的格式化与反射/配置文件里的格式换完全一样
        # print(value)
        target=re.sub(p,value,target,count=1)  #替换一次,赋值给新的字符串
    return target


if __name__ == '__main__':
    target="{'mobilephone':'#normal_phone#','pwd':'#normal_pwd#'}"
    print(replace(target))


    # print(GetData.cookies)  # 类名直接调用属性取值
    # print(GetData().cookies)    #实例化调用属性 取值
    #
    # # 利用反射的机制 取值
    # # 第一个参数是类名，第二个参数是属性的参数名
    # print(getattr(GetData,'cookies'))   #取值
    # print(setattr(GetData,'cookies','lemon'))   #重新赋值
    # print(hasattr(GetData,'cookies'))   #判断是否有属性值
    # print(getattr(GetData,'cookies'))
    # print(delattr(GetData,'cookies'))   #删除属性