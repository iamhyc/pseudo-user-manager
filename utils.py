#!/usr/bin/env python3
import os
from pathlib import Path

PSEUDO_USER  = os.getenv('PSEUDO_USER')
USER_SHELL = os.getenv('SHELL')
USER_HOME = Path(
    os.popen('getent passwd "$USER" | cut -d: -f6').read().strip()
)

DB_FILE = Path(USER_HOME, '.pseudo-user/persistence.db')

def expand_pseudo_home(name:str) -> Path:
    return USER_HOME / name
