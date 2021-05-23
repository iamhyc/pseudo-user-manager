#!/usr/bin/env python3
import os, sys, sqlite3
from pathlib import Path
import getpass, password
from utils import *

# homedir=$( getent passwd "$USER" | cut -d: -f6 )

def expand_pseudo_home(name:str) -> Path:
    return USER_HOME / name

def switch_context(name):
    _home = expand_pseudo_home(name)
    os.environ['HOME'] = _home.as_posix()
    os.environ['XDG_CACHE_HOME']  = (_home/'.cache').as_posix()
    os.environ['XDG_CONFIG_HOME'] = (_home/'.config').as_posix()
    os.environ['XDG_DATA_HOME']   = (_home/'.data').as_posix()
    os.putenv('PSEUDO_USER', name)
    os.chdir(_home)
    os.execv(USER_SHELL)
    pass

def verify_password(name:str) -> bool:
    count = 0
    flag  = False
    #TODO: fetch the user password here
    _pass = password.Password(method='sha256', hash_encoding='base64')

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

def main(name):
    if not expand_pseudo_home(name).exists():
        raise Exception('No pseudo user "%s" exists.'%name)
    if not verify_password(name):
        raise Exception('Wrong password.')
    switch_context(name)
    pass

def login():
    print('Pseudo User Login Interface')
    name = None
    while not name:
        name = input('Login: ').strip()
    main(name)
    pass

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            login()
        else:
            main(sys.argv[1])
    except Exception as e:
        raise e #print(e)
    finally:
        pass #exit()