# -*- coding: utf-8 -*-
import requests

class HttpRequest:
    '''完成http的get 以及post请求，并返回结果'''
    def http_request(self,method,url,param,cookies):
        '''根据请求方法来决定发起get请求还是post请求
        method: get post http的请求方式
        url:发送请求的接口地址
        param:随接口发送的请求参数 以字典格式传递
        rtype:有返回值，返回结果是响应报文
        '''
        global resp
        if method.upper()=='GET':
            try:
                resp=requests.get(url,params=param,cookies=cookies)
            except Exception as e:
                print('get请求出错：{}'.format(e))
        elif method.upper()=='POST':
            try:
                resp=requests.post(url,data=param,cookies=cookies)
            except Exception as e:
                print('post请求出错：{}'.format(e))
        else:
            print('不支持该种方式')
            resp=None
        return resp #直接返回resp，后续调用时可以根据需要打印text 或者 json格式

#测试代码
if __name__ == '__main__':
    # url='http://47.107.168.87:8080/futureloan/mvc/api/member/register'#接口地址
    url1 = 'http://test.lemonban.com/futureloan/mvc/api/member/register'
    param={'mobilephone':'18813989999','pwd':'123456','regname':'lemonhuahua'}#字典的形式存储参数数据
    method='get'

    resp=HttpRequest().http_request(method,url1,param,cookies=None)
    print(resp.text)
    print(resp.headers)
    print(resp.json())

    # print(resp.cookies)