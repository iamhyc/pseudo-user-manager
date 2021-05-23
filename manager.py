#!/usr/bin/env python3
import os, sys, argparse
from pathlib import Path
import getpass, password
import shutil
from utils import *

def db_init(reset=False):
    if not DB_FILE.exists():
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        DB_FILE.touch()
        ACCOUNT_DB.create()
        pass

def useradd_base(name:str):
    _pseudo = expand_pseudo_home(name)
    _pseudo.mkdir(parents=True, exist_ok=True)
    for _base in ['Downloads', 'Documents', 'Pictures']:
        (_pseudo/_base).mkdir(parents=True, exist_ok=True)
    #
    _yes = lambda x: (USER_HOME/x).exists() and not (_pseudo/x).exists()
    basefiles = ['.bashrc', '.zshrc', '.zshenv', '.oh-my-zsh']
    for _base in basefiles:
        if _yes(_base):
            try:
                shutil.copy2(USER_HOME/_base, _pseudo)
            except:
                shutil.copytree(USER_HOME/_base, _pseudo/_base)
    pass

def useradd(name:str) -> tuple: # (bool, str)
    if ACCOUNT_DB.get(name):
        return (False, 'No user "%s" exists.'%name)
    #
    p1 = getpass.getpass('Password: ')
    p2 = getpass.getpass('Password again: ')
    if p1!=p2:
        return (False, 'Password not match.')
    else:
        _pass = password.Password(method='sha256', hash_encoding='base64')
        _pass = p1
        ACCOUNT_DB.add(name, _pass, 'sha256')
        useradd_base(name)
        return (True, '')
    pass

def userdel(name:str, force:bool=False) -> tuple: #(bool, str)
    _row = ACCOUNT_DB.get(name)
    if _row:
        _pass = password.Password(method='sha256', hash_encoding='base64')
        _pass = _row[1]
        if getpass.getpass() == _pass:
            ACCOUNT_DB.delete(name)
            return (True, '')
        else:
            return (False, 'Wrong password.')
    else:
        return (False, 'No user %s exists.'%name)
    pass

def usermod(name) -> tuple: #(bool, str)
    WARNING_MSG('Unimplemented!')
    return (True, '')

def userls():
    _users = ACCOUNT_DB.getAll()
    for _user in _users: print(_user[0])
    pass

def main():
    db_init()
    parser = argparse.ArgumentParser(description='Pseudo-user manager.')
    parser.add_argument('--init', dest='init_flag', action='store_true',
        help='(Optional) initialize the persistence database.')
    parser.add_argument('--add', dest='add_name', metavar='pseudo_name',
        help='add one pseudo user.')
    parser.add_argument('--delete', dest='del_name', metavar='pseudo_name',
        help='delete existing pseudo user.')
    parser.add_argument('--modify', dest='mod_name', metavar='pseudo_name',
        help='modify existing pseudo user.')
    parser.add_argument('--list', dest='list_flag', action='store_true',
        help='list existing pseudo users.')
    args = parser.parse_args()
    #
    if args.init_flag:
        db_init()
    if args.add_name:
        flag, msg = useradd(args.add_name)
        if not flag: ERROR_MSG(msg)
    elif args.del_name:
        flag, msg = userdel(args.del_name)
        if not flag: ERROR_MSG(msg)
    elif args.mod_name:
        flag, msg = usermod(args.mod_name)
        if not flag: ERROR_MSG(msg)
    elif args.list_flag:
        userls()
    pass

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e #pass
    finally:
        pass #exit()
