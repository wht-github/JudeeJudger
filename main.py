import socket
import json
import _judger
import time
import socket
import logging
import threading
import os
import filecmp
import json
import redis
from judeeerrors import *
from PCModel import *
from judgingmethod import judge
import judeesql
from pars import *
'''
Judging Flow:
    1. Get the Submission ID from Judge Server
    2. Get the Corresponding TestCases and code
    3. Compile if necessary
    4. Running for each testcase and recording the result
    5. Update database

Dictionary:
    ProblemData/?/[#.in, #.out] -- ? is the problem id, # is the testcase id
    UserData/?/[#.output, #.error]  -- ? is the User id, # is corresponding to the testcase id

'''


def run():

    while True:
        time.sleep(1)
        if RunningStatus.status:
            RunningStatus.status = False
            try:
                logging.debug('Trying to Get Submission')
                submissionId = get_consumer_from_singlePool(
                    'submission').consume()
                logging.debug('Get Submission ID %s' % submissionId)
                judeesql.update_submission_by_id(submissionId, 7, False)
                submissionInfo = judeesql.get_submission_by_id(
                    submissionId, dic=True)
                t = threading.Thread(target=judge, args=(submissionInfo['ID'], submissionInfo['code'], submissionInfo['language'], submissionInfo['problem_id'],
                                                         submissionInfo['contest_id'], submissionInfo['username_id']))
                t.setDaemon(True)
                t.start()
                RunningStatus.status = True
            except Exception as e:
                raise e


if __name__ == '__main__':
    logging.basicConfig(
        level='DEBUG', format='%(name)s - %(levelname)s - %(message)s')
    GlobalParameters.path_list['python3'] = "/home/wang/Workspace/OJ/env/bin/python"
    run()
    # print('test')
