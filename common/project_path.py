# -*- coding: utf-8 -*-

import os
#文件的路径 放到这里
file_past=os.path.realpath(__file__)
# print(file_past)
project_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
# print(project_path)

#测试用例的路径
case_path=os.path.join(project_path,'test_cases','test_api_1.xlsx')

#日志的路径
log_path=os.path.join(project_path,'test_result','test_log','test.log')

#测试报告的路径
report_path=os.path.join(project_path,'test_result','test_report','前程贷测试报告.html')

#配置文件的路径
conf_path=os.path.join(project_path,'conf','api_test.conf')

if __name__ == '__main__':
    print(file_past)
    print(project_path)
    print(conf_path)
    print(case_path)
