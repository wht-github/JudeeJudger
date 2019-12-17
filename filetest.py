import filecmp
with open('./RT/out.out','r'), open('./ProblemData/1/1.out', 'r') as f1,f2:
    print(f1.read() == f2.read()) 
print(filecmp.cmp('./RT/out.out','./ProblemData/1/1.out',False))