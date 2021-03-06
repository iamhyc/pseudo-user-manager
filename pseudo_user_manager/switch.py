#!/usr/bin/env python3
import os, sys
from pathlib import Path
import getpass, password
from .utils import *

def switch_context(name):
    _home = expand_pseudo_home(name)
    os.environ['HOME'] = _home.as_posix()
    os.environ['XDG_CACHE_HOME']  = (_home/'.cache').as_posix()
    os.environ['XDG_CONFIG_HOME'] = (_home/'.config').as_posix()
    os.environ['XDG_DATA_HOME']   = (_home/'.data').as_posix()
    os.putenv('PSEUDO_USER', name)
    _in_base_home = Path(os.getenv('PWD'))==USER_HOME
    _in_ssh_link  = os.getenv('SSH_CLIENT') or os.getenv('SSH_TTY')
    if _in_base_home and _in_ssh_link:
        os.chdir(_home)
    os.execl(USER_SHELL, USER_SHELL)

def verify_password(name:str) -> bool:
    count = 0
    flag  = False
    #
    _user = ACCOUNT_DB.get(name)
    if not _user:
        return False
    _pass = password.Password(method='sha256', hash_encoding='base64')
    _pass = _user[1]

    _NUM = 3
    while not flag and count<_NUM:
        if count == 0:
            _prompt = 'Password: '
        elif count < _NUM-1:
            _prompt = 'Password [%d trails left]: '%(_NUM-count)
        else:
            _prompt = 'Password [%d trail left]: '%(_NUM-count)
        #
        if getpass.getpass(_prompt) == _pass:
            flag = True
        else:
            print('Wrong password, try again.')
            count += 1
        pass
    return flag

def login_interface():
    print('Pseudo User Login Interface')
    name = input('Login: ').strip()
    return name

def main():
    if len(sys.argv)==2:
        name = sys.argv[1]
    else:
        name = login_interface()
    if not name:
        return
    if not expand_pseudo_home(name).exists():
        raise Exception('No pseudo user "%s" exists.'%name)
    if not verify_password(name):
        raise Exception('Wrong password.')
    switch_context(name)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e #print(e)
    finally:
        pass #exit()