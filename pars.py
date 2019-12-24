import json
class RunningStatus:
    '''
    status is True: Judger is free, vise versa
    '''
    status = True
    judgerName = 'Judee'
    __pj = None
    @classmethod
    def getProblemParas(cls):
        if cls.__pj:
            return cls.__pj
        else:
            with open('./conf.d/problemdata.json', 'r') as f:
                cls.__pj = json.loads(f)
            return cls.__pj
class GlobalParameters:
    db_keys = ['db_ip', 'db_pwd', 'db_user', 'db_port']
    server_keys = ['server_ip', 'server_port', 'key']
    path_keys = ['python3','java','c','cpp']
    db_config = {key : None for key in db_keys}
    path_list = {key : None for key in path_keys}

