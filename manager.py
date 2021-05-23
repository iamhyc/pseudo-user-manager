#!/usr/bin/env python3
import os, sys, sqlite3, argparse
from pathlib import Path
import getpass, password
import shutil
from utils import *

def db_init(reset=False):
    if not DB_FILE.exists():
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        DB_FILE.touch()
        with sqlite3.connect(DB_FILE) as con:
            con.execute('''
                CREATE TABLE default (
                    username text,
                    password text,
                    method text
                );
            ''')
        pass

def useradd_base(name:str):
    _pseudo = expand_pseudo_home(name)
    _yes = lambda x: (USER_HOME/x).exists() and not (_pseudo/x).exists()
    if not _pseudo.exists():
        _pseudo.mkdir(parents=True, exist_ok=True)
    #
    basefiles = ['.bashrc', '.zshrc', '.zshenv', '.oh-my-zsh']
    for _base in basefiles:
        if _yes(_base): shutil.copy(USER_HOME/_base, _pseudo)
    pass

def useradd(name:str) -> tuple: # (bool, str)
    with sqlite3.connect(DB_FILE) as con:
        _row = con.execute('SELECT * FROM default WHERE username = %s'%name)
        if _row:
            return (False, 'No user "%s" exists.'%name)
    #
    p1 = getpass.getpass('Password: ')
    p2 = getpass.getpass('Password again: ')
    if p1!=p2:
        return (False, 'Password not match.')
    else:
        _pass = password.Password(method='sha256', hash_encoding='base64')
        _pass = p1
        _value = str( (name, _pass, 'sha256') )
        with sqlite3.connect(DB_FILE) as con:
            con.execute('''
                INSERT INTO default
                VALUES {value}
            '''.format(value=_value))
        useradd_base(name)
        return (True, '')
    pass

def userdel(name:str) -> tuple: #(bool, str)
    with sqlite3.connect(DB_FILE) as con:
        _row = con.execute('SELECT * FROM default WHERE username = %s'%name)
        if _row:
            _pass = password.Password(method='sha256', hash_encoding='base64')
            _pass = _row[1]
            if getpass.getpass() == _pass:
                con.execute('DELETE FROM default WHERE username = %s'%name)
                return (True, '')
            else:
                return (False, 'Wrong password.')
        else:
            return (False, 'No user %s exists.'%name)
    pass

def usermod(name):
    print('Unimplemented.')
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
    args = parser.parse_args()
    #
    if args.init_flag:
        db_init()
    if args.add_name:
        useradd(args.add_name)
    elif args.del_name:
        userdel(args.del_name)
    elif args.mod_name:
        usermod(args.mod_name)
    pass

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e #pass
    finally:
        pass #exit()
