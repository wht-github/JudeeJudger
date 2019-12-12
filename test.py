# coding=utf-8
import _judger
import json
import pars
import judgingmethod
# import judeesql
from PCModel import get_consumer_from_singlePool
import logging
from judeeerrors import *
python3path = "/home/wang/Workspace/OJ/env/bin/python"

if __name__ == '__main__':
    logging.basicConfig(
        level='DEBUG', format='%(name)s - %(levelname)s - %(message)s')
    submissionId = get_consumer_from_singlePool(
        'submission').consume()
    print(submissionId)
    # with open('aaa.c', 'r') as f:
    #     code = f.read()
    # try:
    #     judgingmethod.judge('1', code, 'C', '1', '0', '5')
    # except CompilerError as e:
    #     print('ee')
    #     raise e
    # a = judeesql.get_submission_by_id(1,dic=True)
    # print(a)
    # print(pars.RunningStatus.status)
    # print(pars.RunningStatus.status)
    #   a = judgePython3(1000,100,'/home/wang/Workspace/OJ/Judee/in.txt','/home/wang/Workspace/OJ/Judee/out.txt','/home/wang/Workspace/OJ/Judee/err.txt',0,'/home/wang/Workspace/OJ/Judee/a_b')
    #   a['result'] = a['result']
    #   f = json.dumps(a)
    #   print(f)
