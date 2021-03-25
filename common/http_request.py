# -*- coding: utf-8 -*-
import requests
from common.get_token import Token

class HttpRequest:
    '''完成http的get 以及post请求，并返回结果'''

    # def __init__(self):
    #     self.cookie = Token().get_token()


    def http_request(self,method,url,param,cookies=None):
        '''根据请求方法来决定发起get请求还是post请求
        :param method: get post http的请求方式
        :param url:发送请求的接口地址
        :param param:随接口发送的请求参数 以字典格式传递
        :param rtype:有返回值，返回结果是响应报文
        '''
        global resp
        if not url.startswith('http://'):
            url = 'http://{}'.format(url)
            print(url)

        if method.upper()=='GET':
            try:
                # resp=requests.get(url,params=param,cookies = self.cookie)
                resp = requests.get(url, params=param,cookies=cookies)
            except Exception as e:
                print('get请求出错：{}'.format(e))
            time_consuming = resp.elapsed.microseconds/1000
            time_total = resp.elapsed.total_seconds()
            # 接口响应时间list，单位毫秒
            STRESS_LIST = []

            # 接口执行结果list
            RESULT_LIST = []
            STRESS_LIST.append(time_consuming)

            # response_dicts = dict()
            # response_dicts['code'] = resp.status_code
            # try:
            #     response_dicts['body'] = resp.json()
            # except Exception as e:
            #     print(e)
            #     response_dicts['body'] = ''
            # # response_dicts['text'] = resp.text
            # response_dicts['time_consuming'] = time_consuming
            # response_dicts['time_total'] = time_total
            # return response_dicts

            return resp


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
    url = 'http://test.lemonban.com/futureloan/mvc/api/member/login'
    param={'mobilephone':'18813989999','pwd':'123456','regname':'lemonhuahua'}#字典的形式存储参数数据
    method='get'

    resp=HttpRequest().http_request(method,url,param)
    # print(resp.text)
    # print(resp.headers)
    # print(resp.json())
    print(resp.cookies)

    # print(resp.cookies)