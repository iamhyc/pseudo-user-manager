#!/usr/bin/env python3
import os, sys, sqlite3
from pathlib import Path
import getpass, password
from utils import *

def db_init():
    if not DB_FILE.exists():
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        DB_FILE.touch()
        #TODO: init the table
        pass

def useradd(name):
    pass

def userdel(name):
    pass

def usermod(name):
    pass

def main():
    db_init()
    # parse args here:
    #   - useradd, userdel, usermod
    pass

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e #pass
    finally:
        pass #exit()
