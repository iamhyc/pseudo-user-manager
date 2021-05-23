#!/usr/bin/env python3
from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name = 'pseudo-user-manager',
        version = '0.1.0',
        description = 'Pseudo-user manager for remote ssh use.',
        author = 'iamhyc',
        author_email = 'sudofree@163.com',
        #
        install_requires = ['password', 'termcolor'],
        package_dir = {'': './'},
        packages = find_packages(where='./'),
        package_data = {},
        entry_points = {
            'console_scripts': [
                'pseudo-manager = pseudo_user_manager:manager:main',
                'pseudo-switch = pseudo_user_manager:switch:main'
            ]
        }
    )