import os
from pars import RunningStatus as rs
def PackupTestcases(problem):
    testcases = os.listdir('./ProblemData/%s/' % problem)
    in_list = [i for i in testcases if i.split('.')[1] == 'in']
    out_list = [i for i in testcases if i.split('.')[1] == 'out']
    in_list = sorted(in_list)
    out_list = sorted(out_list)
    tests = zip(in_list,out_list)
    return tests
def rsync(problemid):
    pd = rs.getProblemParas()
    # print('sshpass -p "%s" rsync -r  %s:%s/%s /JudeeJudger/ProblemData/ --delete' % (pd['password'], pd['hostaddress'], pd['remotedatapath'], str(problemid)))
    os.system('sshpass -p "%s" rsync -r  %s:%s/%s /JudeeJudger/ProblemData/ --delete' % (pd['password'], pd['hostaddress'], pd['remotedatapath'], str(problemid)))


