def judgeJava(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):

    com1 = "/usr/bin/time -f '"+"%"+"U' -o %stime.txt " % (judgername)
    com2 = "timeout %s java -cp %s -Djava.security.manager -Djava.security.policy==policy -Djava.awt.headless=true Main 1>%s 2>%s<%s" % (
        str(timelimit/1000.0), judgername, outputpath, errorpath, inputpath)
    com = com1 + com2
    result = os.system(com)

    ret = dict()

    if result == 0:
        tf = open(judgername+"time.txt", "r")
        time = tf.read()
        time = float(str(time).strip())*1000
        ret["cpu_time"] = int(time)
        ret["memory"] = 5201314
        ret["result"] = 0
        ret["exit_code"] = result
        ret["signal"] = 0
        tf.close()
    elif result == 31744:
        ret["cpu_time"] = timelimit
        ret["memory"] = 5201314
        ret["result"] = 1
        ret["exit_code"] = result
        ret["signal"] = 0
    else:
        tf = open(errorpath, "r")
        msg = tf.read()
        GlobalVar.cursor.execute(
            "UPDATE judgestatus_judgestatus SET message=%s WHERE id = %s", (msg, id))
        GlobalVar.db.commit()
        ret["cpu_time"] = 0
        ret["memory"] = 5201314
        ret["result"] = 4
        ret["exit_code"] = result
        ret["signal"] = 0
        tf.close()

    return ret

def compileJava(id,code,judgername,problem):
    file = open("Main.java", "w",encoding='utf-8')
    file.write(code)
    file.close()

    isExists = os.path.exists(judgername)
    if not isExists:
        os.makedirs(judgername)

    result = os.system("javac Main.java -d %s 2>%sce.txt" % (judgername, judgername))

    if result:
        try:
            filece = open("%sce.txt" % judgername, "r")
            msg = str(filece.read())
            filece.close()
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        except:
            msg = str("Fatal Compile error!")
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        return False
    return True