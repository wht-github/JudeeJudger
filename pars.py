import json
class RunningStatus:
    status = True
    judgerName = 'Judee'

class GlobalParameters:
    db_keys = ['db_ip', 'db_pwd', 'db_user', 'db_port']
    server_keys = ['server_ip', 'server_port', 'key']
    path_keys = ['python3','java','c','cpp']
    db_config = {key : None for key in db_keys}
    path_list = {key : None for key in path_keys}
    @staticmethod
    def init_path(pathname,systempath):
        path_list[pathname] = systempath

