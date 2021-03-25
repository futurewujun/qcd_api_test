# -*- coding: utf-8 -*-

from mysql import connector
from pymysql import Connect
from common.read_config import ReadConfig
from common import project_path
class DoSql:
    '''操作数据库，进行数据的读取'''
    def do_sql(self,query,flag=1):
        '''query:查询语句
           flag：标记，1：查询第一条数据，2：查询获取多条的数据'''
        # 读取配置文件的数据库信息，连接数据库，
        db_config=ReadConfig().get_data('DB','db_config') # 数据库基本信息
        # cnn=connector.connect(**db_config)  #建立连接
        cnn1 = Connect(**db_config)
        # 获取游标
        # cursor=cnn.cursor()
        cursor=cnn1.cursor()
        # 操作数据表， 执行查询语句
        cursor.execute(query)
        # 判断flag，要获取哪些数据
        if flag==1:
            res=cursor.fetchone()   #查询第一条数据，返回的是元祖类型
        else:
            res=cursor.fetchall()   #查询所有的数据，返回的是列表嵌套元祖类型
        cnn1.close()
        cursor.close()
        return res
if __name__ == '__main__':
    query='SELECT MAX(Id) FROM loan WHERE loan.MemberID=1126351'
    query_1='SELECT leaveamount FROM member WHERE Id = 1126351'
    re=DoSql().do_sql(query,1)
    re_1=DoSql().do_sql(query_1,1)
    print(re)
    print(re_1)
    print(re_1[0])
    print(type(re_1))

'''如果是增删改的话，执行语句之后，要提交：
# cursor.execute(query)
# cursor.execute('commit')    # 提交
'''