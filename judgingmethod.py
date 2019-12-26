import _judger
import os
from judeeerrors import *
from judgeutils import *
from pars import *
import logging
import json
import filecmp
import tempfile
from pars import *
# from judeesql import update_submission_by_id, update_ocrank_by_cid_uid, get_contest_type, get_problem_info, update_submission_userdata, update_problem,*
from judeesql import *
logger = logging.getLogger("root")
# logger.basicConfig(
#     level='DEBUG', format='%(name)s - %(levelname)s - %(message)s',)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())
def judgePython3(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    logger.debug(GlobalParameters.path_list['python3'])
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
def judgeJava(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    print('-cp %s -XX:MaxRAM=%dk -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main' % ('./RT/'+str(id)+'/', 1024*3*memorylimit))
    return _judger.run(max_cpu_time=timelimit,
                       max_real_time=timelimit*10,
                       max_memory=-1,
                       max_process_number=200,
                       max_output_size=-1,
                       max_stack=-1,
                       # five args above can be _judger.UNLIMITED
                       exe_path="java"+'-cp %s -XX:MaxRAM=%dk -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main' % ('./RT/'+str(id)+'/', 800*1024),
                       input_path=inputpath,
                       output_path=outputpath,
                       error_path=errorpath,
                       args=[],
                       # can be empty list
                       env=[],
                       log_path=judgername+"judger.log",
                       # can be None
                       seccomp_rule_name=None,
                       uid=0,
                       gid=0
                       )


def compileC(id, code, workpath):
    # transfer code into file named with judgername
    tmp_name = workpath+'/'+str(id)
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


def compileCPP(id, code, workpath):
    tmp_name = workpath+'/'+str(id)
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


def compilePython3(id, code, workpath):
    tmp_name = workpath+'/'+ str(id)
    # file.write("import sys\nblacklist = ['importlib','traceback','os']\nfor mod in blacklist:\n    i = __import__(mod)\n    sys.modules[mod] = None\ndel __builtins__.__dict__['eval']\ndel __builtins__.__dict__['exec']\ndel __builtins__.__dict__['locals']\ndel __builtins__.__dict__['open']\n" +code)
    with open("%s.py" % tmp_name, "w", encoding='utf-8') as f:
        f.write(code)
def compileJava(id,code,workpath):
    tmp_name = workpath+'/'+'Main.java'
    cepath = workpath + '/' +'ce.txt'
    with open(tmp_name, 'w', encoding='utf-8') as f:
        f.write(code)

    result = os.system("javac %s -d %s 2>%s" %
                       (tmp_name, workpath, cepath))
    if result != 0:
        try:
            with open(cepath, 'r') as f:
                msg = str(f.read())
            if msg == '':
                msg = 'Compile timeout! Maybe you define too big arrays!'
            raise CompilerError(msg)
        except FileNotFoundError:
            msg = str('Fatal Compile error!')
            raise CompilerError(msg)

def judge(id, code, lang, problem, contest, username, createTime):
    '''
        id: submission id
        code: submission code
        lang: submission language
        problem: problem id
        contest: 属于哪个比赛的提交，为0时，不属于任何比赛的提交
        username: user id
    '''
    logger.debug('Synchonizing the TestCases')
    # os.system('sshpass -p "hhs123456" rsync -r  h2s@snail.leeeung.com:/volume4/homes/h2s/test_cases/ /home/wang/Workspace/OJ/Judee/ProblemData/ --delete')
    rsync(problem)
    logger.debug('Synchonizing Finished')

    rule = ''
    if contest is not None:
        rule = get_contest_type(contest).rule_type
    problemInfo = get_problem_info(problem, True)
    timelimit = int(problemInfo['time_limit'])
    memorylimit = int(problemInfo['memory_limit'])
    testcaseScore = problemInfo['test_case_score'] 
    logger.debug('MemoryLimit: %d TimeLimit: %d' % (memorylimit, timelimit))

    retnum = 0
    info = []
    result_list = []
    total_score = 0
    try:
        tests = PackupTestcases(problem)
        workpath ='./RT/%s' % str(id)
        if not os.path.exists('./RT/%s' % str(id)):
            os.makedirs(workpath)
        if lang == 'C':
            compileC(id, code, workpath)
        elif lang == 'C++':
            compileCPP(id, code, workpath)
        elif lang == 'Python3':
            compilePython3(id, code, workpath)
        elif lang == 'Java':
            compileJava(id,code,workpath)
        else:
            raise Exception('No language support')

        for incase, outcase in tests:
            caseid = incase.split('.')[0]
            logger.debug('Judging %s %s' % (incase, outcase))
            incasePath = './ProblemData/%s/%s' % (problem, incase)
            outcasePath = './ProblemData/%s/%s' % (problem, outcase)
            # outputPath = './UserData/%s/%s/%s' % (username, problem, outcase)
            # errorPath = './UserData/%s/%s/%s' % (username, problem, caseid)
            outputPath = '%s/out_%s.txt' % (workpath,str(id))
            errorPath = '%s/error_%s.txt' % (workpath,str(id))
            # logger.info('go')
            logpath = '%s/%s' % (workpath, str(id))
            if lang == 'C':
                result = judgeC(timelimit, memorylimit, incasePath,
                                outputPath, errorPath, id, logpath)
            elif lang == 'C++':
                result = judgeCPP(timelimit, memorylimit, incasePath,
                                  outputPath, errorPath, id, logpath)
            elif lang == 'Python3':
                result = judgePython3(timelimit, memorylimit, incasePath,
                                      outputPath, errorPath, id,logpath)
            elif lang == 'Java':
                result = judgeJava(timelimit, memorylimit, incasePath,
                                      outputPath, errorPath, id,logpath)
            if result['result'] == 0 and result['error'] == 0:
                logger.debug('Running Successfully')
                # tmp = 0 if filecmp.cmp(outcasePath, outputPath,False) else -1
                cmp_info = os.system('diff --strip-trailing-cr --ignore-trailing-space %s %s' %(outcasePath, outputPath))
                tmp = 0 if cmp_info == 0 else -1
                if retnum == 0:
                    retnum = tmp
                result['result'] = tmp
                if retnum == 0:
                    total_score += testcaseScore[int(caseid)-1]
                logger.debug('case %d result is %d' % (int(caseid), result['result']))
            else:
                retnum = result['result']
                logger.debug('case failed with %d' % retnum)

            with open(errorPath, 'r') as errordata:
                result['error_info'] = errordata.read()
            with open('%s/%sjudger.log' % (workpath,str(id)),'r') as f:
                result['error_info'] += f.read()
            result_list.append(result)

        print(result_list)
    except NotADirectoryError:
        logger.debug('./ProblemData/%s/ not exist' % problem)
        update_submission(id, 5)
        raise Exception('no testing data')
        # Update the Database

    except CompilerError as e:
        compilemsg = e.args
        logger.debug('Compile Error %s' % compilemsg)
        update_problem(problem,username,-2)
        # update_submission_by_id(id,-2,compilemsg)
        update_submission(id, -2, compile_error_info=compilemsg)
        if rule == 'ACM':
            update_acm_rank(contest, username, problem, createTime, -2)
        elif rule == 'OI':
            update_oi_rank(contest,username,problem,total_score)
        Running_Status = True
        # raise e

    except Exception as e:
        update_submission(id, 5)
        raise e
    else:
        logger.debug('All success')
        if rule == 'ACM':
            update_acm_rank(contest, username, problem, createTime, retnum)
        elif rule == 'OI':
            update_oi_rank(contest,username,problem,total_score)
        update_problem(problem,username,retnum)
        # update_submission_userdata(id,retnum,result_list,username,problem,testcaseScore)
        update_submission(id, retnum, info=result_list)
        Running_Status = True
    # finally:
    #     Running_Status = True

    # finally:
    #     # update_submission_by_id(id,)
    #     Running_Status = True
    #     return
