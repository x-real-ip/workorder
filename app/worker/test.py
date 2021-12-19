import os

base_path = '/app'
worker_path = base_path + '/worker'
log_path = base_path + '/log'
db_path = base_path + '/db'

env_variables = ('WEB_URL', 'WEB_USERNAME', 'WEB_PASSWORD')


def check_env(var):
    for var in env_variables:
        if var in os.environ:
            if os.environ[var] == "":
                print(f'{var} is empty, please set a value')
        else:
            print(f'{var} does not exist, please setup this env variable')


check_env(env_variables)
