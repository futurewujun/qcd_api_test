# -*- coding: utf-8 -*-
import logging
from common import project_path
class MyLog:
    '''自定义的日志类'''
    def my_log(self,level,msg):
        my_logger=logging.getLogger('testing_log')  #定义一个日志收集器，并且命名
        my_logger.setLevel('DEBUG') #设置日志收集器级别
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-[%(name)s]-[日志信息]:%(message)s')  # 设置日志格式
        sh=logging.StreamHandler()  #设置输出到控制台
        sh.setLevel('DEBUG')    #设置级别
        sh.setFormatter(formatter)  #设置输出到控制台的格式
        fh=logging.FileHandler(project_path.log_path,encoding='utf-8')  #设置输出到文本
        fh.setLevel('DEBUG')    #设置级别
        fh.setFormatter(formatter)  #设置输出到文本的格式
        # 将设置的输出方式添加到设置的收集器，对接-取两者交集
        my_logger.addHandler(sh)
        my_logger.addHandler(fh)

        if level == 'DEBUG':
            my_logger.debug(msg)
        elif level == 'INFO':
            my_logger.info(msg)
        elif level == 'WARNING':
            my_logger.warning(msg)
        elif level == 'ERROR':
            my_logger.error(msg)
        else:
            my_logger.critical(msg)
        # 最后必须移除
        my_logger.removeHandler(fh)
        my_logger.removeHandler(sh)
    def debug(self,msg):
        self.my_log('DEBUG',msg)    #调用my_log函数
    def info(self,msg):
        self.my_log('INFO',msg)
    def error(self,msg):
        self.my_log('ERROR',msg)
    def warning(self,msg):
        self.my_log('WARNING',msg)
    def critical(self,msg):
        self.my_log('CRITICAL',msg)

    # def read_case(self):
    #     ''''''
    #
    #     try:
    #         self.info('开始执行用例')
    #         DoExcel().('test_case.xlsx', 'Sheet1')
    #         self.info('数据读取完毕')
    #     except Exception as e:
    #         # print('数据读取失败，错误是:{}'.format(e))
    #         self.error(e)
    #         self.info('数据读取失败')
if __name__ == '__main__':
    my_log=MyLog()
    my_log.info('开始测试')
