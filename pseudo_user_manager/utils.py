#!/usr/bin/env python3
import os
from pathlib import Path
import sqlite3
from termcolor import cprint

PSEUDO_USER  = os.getenv('PSEUDO_USER')
USER_SHELL = os.getenv('SHELL')
USER_HOME = Path(
    os.popen('getent passwd "$USER" | cut -d: -f6').read().strip()
)
DB_FILE = Path(USER_HOME, '.pseudo-users/persistence.db')

ERROR_MSG   = lambda x: cprint(str(x), 'red')
WARNING_MSG = lambda x: cprint(str(x), 'yellow')
SUCCESS_MSG = lambda x: cprint(str(x), 'green')

def expand_pseudo_home(name:str) -> Path:
    return USER_HOME / name

class ACCOUNT_DB:
    @staticmethod
    def create():
        with sqlite3.connect(DB_FILE) as con:
            con.execute('''
                CREATE TABLE account (
                    username text unique,
                    password text,
                    method text
                )
            ''')
        pass

    @staticmethod
    def get(name):
        with sqlite3.connect(DB_FILE) as con:
            _cur = con.execute('SELECT * FROM account WHERE username = "%s"'%name)
            return _cur.fetchone()
        pass

    @staticmethod
    def getAll():
        with sqlite3.connect(DB_FILE) as con:
            _cur = con.execute('SELECT * FROM account')
            return _cur.fetchall()

    @staticmethod
    def add(name, password, method='sha256'):
        with sqlite3.connect(DB_FILE) as con:
            con.execute('''
                INSERT INTO account
                VALUES (?, ?, ?)
            ''', (name, password, method))
        pass

    @staticmethod
    def update(name):
        pass

    @staticmethod
    def delete(name):
        with sqlite3.connect(DB_FILE) as con:
            con.execute('DELETE FROM account WHERE username = "%s"'%name)
        pass

    @staticmethod
    def destroy():
        pass

    pass
