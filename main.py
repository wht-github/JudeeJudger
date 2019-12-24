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
logger = logging.getLogger("root")
# logger.basicConfig(level='DEBUG', format='%(name)s - %(levelname)s - %(message)s',)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
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
CODE:
    -2: "COMPILE_ERROR",
    -1: "WRONG_ANSWER",
    0: "ACCEPTED",
    1: "CPU_TIME_LIMIT_EXCEEDED",
    2: "REAL_TIME_LIMIT_EXCEEDED",
    3: "MEMORY_LIMIT_EXCEEDED",
    4: "RUNTIME_ERROR",
    5: "SYSTEM_ERROR",
    6: "PENDING",
    7: "JUDGING",
    8: "PARTIALLY_ACCEPTED",

'''


def run():

    while True:
        time.sleep(1)
        if RunningStatus.status:
            RunningStatus.status = False
            try:
                logger.debug('Trying to Get Submission')
                submissionId = get_consumer_from_singlePool(
                    'submission').consume()
                logger.debug('Get Submission ID %s' % submissionId)
                judeesql.update_submission(submissionId, 7)
                submissionInfo = judeesql.get_submission_by_id(
                    submissionId, dic=True)
                logger.debug('Judging Submission %s' % submissionId)

                t = threading.Thread(target=judge, args=(submissionInfo['ID'], submissionInfo['code'], submissionInfo['language'], submissionInfo['problem_id'],
                                                         submissionInfo['contest_id'], submissionInfo['username_id'], submissionInfo['create_time']))
                t.setDaemon(True)
                t.start()
                RunningStatus.status = True
            except Exception as e:
                raise e


if __name__ == '__main__':
    # logger = logging.getLogger("root")
    # logger.basicConfig(
        # level='DEBUG', format='%(name)s - %(levelname)s - %(message)s',)
    GlobalParameters.path_list['python3'] = "/usr/bin/python3.7"
    run()
    # print('test')
