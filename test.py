# coding=utf-8
import _judger
import json
import pars
import judgingmethod
# import judeesql
from PCModel import get_consumer_from_singlePool
import logging
from judeeerrors import *
import os
python3path = "/home/wang/Workspace/OJ/env/bin/python"
def judgePython3(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    # logging.debug(GlobalParameters.path_list['python3'])
    return _judger.run(max_cpu_time=timelimit,
                       max_real_time=timelimit*10,
                       max_memory=memorylimit * 1024 * 1024,
                       max_process_number=200,
                       max_output_size=32 * 1024 * 1024,
                       max_stack=32 * 1024 * 1024,
                       # five args above can be _judger.UNLIMITED
                       exe_path=python3path,
                       input_path=inputpath,
                       output_path=outputpath,
                       error_path=errorpath,
                       args=[judgername+".py"],
                       # can be empty list
                       env=[],
                       log_path=judgername+"judger.log",
                       # can be None
                       seccomp_rule_name="general",
                       uid=0,
                       gid=0
                       )
if __name__ == '__main__':
    a = os.system('diff --strip-trailing-cr ./RT/out.txt ./ProblemData/39/5.ut')
    print(a)
    # logging.basicConfig(
    #     level='DEBUG', format='%(name)s - %(levelname)s - %(message)s')
    # submissionId = get_consumer_from_singlePool(
    #     'submission').consume()
    # print(submissionId)
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
    # a = judgePython3(1000,100,'/home/wang/Workspace/OJ/Judee/in.txt','/home/wang/Workspace/OJ/Judee/out.txt','/home/wang/Workspace/OJ/Judee/err.txt',0,'/home/wang/Workspace/OJ/Judee/a_b')
    # print(a)
    #   a['result'] = a['result']
    #   f = json.dumps(a)
    #   print(f
