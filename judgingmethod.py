import _judger
import os
from judeeerrors import *
from judgeutils import *
from pars import *
import logging
import filecmp
from pars import *
from judeesql import update_submission_by_id, update_ocrank_by_cid_uid, get_contest_type, get_problem_info, update_submission_userdata, update_problem_by_id


def judgePython3(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    logging.debug(GlobalParameters.path_list['python3'])
    return _judger.run(max_cpu_time=timelimit,
                       max_real_time=timelimit*10,
                       max_memory=memorylimit * 1024 * 1024,
                       max_process_number=200,
                       max_output_size=32 * 1024 * 1024,
                       max_stack=32 * 1024 * 1024,
                       # five args above can be _judger.UNLIMITED
                       exe_path=GlobalParameters.path_list['python3'],
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


def judgeC(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    return _judger.run(max_cpu_time=timelimit,
                       max_real_time=timelimit*10,
                       max_memory=memorylimit * 1024 * 1024,
                       max_process_number=200,
                       max_output_size=32 * 1024 * 1024,
                       max_stack=32 * 1024 * 1024,
                       # five args above can be _judger.UNLIMITED
                       exe_path=judgername+".out",
                       input_path=inputpath,
                       output_path=outputpath,
                       error_path=errorpath,
                       args=[],
                       # can be empty list
                       env=[],
                       log_path=judgername+"judger.log",
                       # can be None
                       seccomp_rule_name="c_cpp",
                       uid=0,
                       gid=0
                       )


def judgeCPP(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    return _judger.run(max_cpu_time=timelimit,
                       max_real_time=timelimit*10,
                       max_memory=memorylimit * 1024 * 1024,
                       max_process_number=200,
                       max_output_size=32 * 1024 * 1024,
                       max_stack=32 * 1024 * 1024,
                       # five args above can be _judger.UNLIMITED
                       exe_path=judgername+".out",
                       input_path=inputpath,
                       output_path=outputpath,
                       error_path=errorpath,
                       args=[],
                       # can be empty list
                       env=[],
                       log_path=judgername+"judger.log",
                       # can be None
                       seccomp_rule_name="c_cpp",
                       uid=0,
                       gid=0
                       )


def compileC(id, code, problem):
    # transfer code into file named with judgername
    tmp_name = 'tmp_'+str(problem)
    with open('%s.c' % tmp_name, 'w', encoding='utf-8') as f:
        f.write(code)

    result = os.system('timeout 10 gcc %s.c -fmax-errors=3 -o %s.out -O2 -std=c11 2>%sce.txt' %
                       (tmp_name, tmp_name, tmp_name))
    # print(result)
    if result != 0:
        try:
            with open('%sce.txt' % tmp_name, 'r') as f:
                msg = str(f.read())
            if msg == '':
                msg = 'Compile timeout! Maybe you define too big arrays!'
            # print(msg)
            raise CompilerError(msg)
        except FileNotFoundError:
            msg = str('Fatal Compile error!')
            raise CompilerError(msg)


def compileCPP(id, code, problem):
    tmp_name = 'tmp_'+str(problem)
    with open('%s.cpp' % tmp_name, 'w', encoding='utf-8') as f:
        f.write(code)

    result = os.system("timeout 10 g++ %s.cpp -fmax-errors=3 -o %s.out -O2 -std=c++14 2>%sce.txt" %
                       (tmp_name, tmp_name, tmp_name))
    if result != 0:
        try:
            with open('%sce.txt' % tmp_name, 'r') as f:
                msg = str(f.read())
            if msg == '':
                msg = 'Compile timeout! Maybe you define too big arrays!'
            raise CompilerError(msg)
        except FileNotFoundError:
            msg = str('Fatal Compile error!')
            raise CompilerError(msg)


def compilePython3(id, code, problem):
    tmp_name = 'tmp_' + str(problem)
    # file.write("import sys\nblacklist = ['importlib','traceback','os']\nfor mod in blacklist:\n    i = __import__(mod)\n    sys.modules[mod] = None\ndel __builtins__.__dict__['eval']\ndel __builtins__.__dict__['exec']\ndel __builtins__.__dict__['locals']\ndel __builtins__.__dict__['open']\n" +code)
    with open("%s.py" % tmp_name, "w", encoding='utf-8') as f:
        f.write(code)


def judge(id, code, lang, problem, contest, username):
    '''
        id: submission id
        code: submission code
        lang: submission language
        problem: problem id
        contest: 属于哪个比赛的提交，为0时，不属于任何比赛的提交
        username: user id
    '''
    logging.debug('Synchonizing the TestCases')
    os.system('sshpass -p "hhs123456" rsync -r  h2s@snail.leeeung.com:/volume4/homes/h2s/test_cases/ /home/wang/Workspace/OJ/Judee/ProblemData/ --delete')
    logging.debug('Synchonizing Finished')

    rule = ''
    if contest is not None:
        rule = get_contest_type(id).rule_type
    problemInfo = get_problem_info(problem, True)
    timelimit = int(problemInfo['time_limit'])
    memorylimit = int(problemInfo['memory_limit'])
    testcaseScore = problemInfo['test_case_score'] 
    logging.debug('MemoryLimit: %d TimeLimit: %d' % (memorylimit, timelimit))

    retnum = 0
    info = []
    result_list = []
    try:
        tests = PackupTestcases(problem)

        if lang == 'C':
            compileC(id, code, problem)
        elif lang == 'C++':
            compileCPP(id, code, problem)
        elif lang == 'Python3':
            compilePython3(id, code, problem)
        else:
            raise Exception('No language support')

        for incase, outcase in tests:
            caseid = incase.split('.')[0]
            logging.debug('Judging %s %s' % (incase, outcase))
            incasePath = './ProblemData/%s/%s' % (problem, incase)
            outcasePath = './ProblemData/%s/%s' % (problem, outcase)
            # outputPath = './UserData/%s/%s/%s' % (username, problem, outcase)
            # errorPath = './UserData/%s/%s/%s' % (username, problem, caseid)
            outputPath = './RT/out.txt'
            errorPath = './RT/error.txt'
            # logging.info('go')
            if lang == 'C':
                result = judgeC(timelimit, memorylimit, incasePath,
                                outputPath, errorPath, id, 'tmp_'+str(problem))
            elif lang == 'C++':
                result = judgeCPP(timelimit, memorylimit, incasePath,
                                  outputPath, errorPath, id, 'tmp_'+str(problem))
            elif lang == 'Python3':
                result = judgePython3(timelimit, memorylimit, incasePath,
                                      outputPath, errorPath, id, "tmp_"+str(problem))
            if rule == 'ACM':
                pass
            elif rule == 'OI':
                pass
            else:
                pass

            if result['result'] == 0:
                logging.debug('Running Successfully')
                if retnum == 0:
                    retnum = 0 if filecmp.cmp(outcasePath, outputPath) else -1
                    logging.debug('case result is %d' % retnum)
            else:
                retnum = result['result']
                logging.debug('case failed with %d' % retnum)

            with open(errorPath, 'r') as errordata:
                result['errorinfo'] = errordata.read()
            result_list.append(result)

        print(result_list)
    except NotADirectoryError:
        logging.debug('./ProblemData/%s/ not exist' % problem)
        # Update the Database

    except CompilerError as e:
        compilemsg = e.args
        logging.debug('Compile Error %s' % compilemsg)
        update_problem_by_id(problem,-2)
        update_submission_by_id(id,-2,compilemsg)
        Running_Status = True
        # raise e

    except Exception as e:

        raise e
    else:
        logging.debug('All success')
        update_problem_by_id(problem,retnum)
        update_submission_userdata(id,retnum,result_list,username,problem,testcaseScore)
        Running_Status = True
    # finally:
    #     Running_Status = True

    # finally:
    #     # update_submission_by_id(id,)
    #     Running_Status = True
    #     return
