# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = (2, 3, 0)
__version__ = '.'.join(map(str, VERSION[0:3]))
__description__ = '''Yet another leetcode cli'''
__author__ = 'zk'
__author_email__ = ''
__homepage__ = 'https://github.com/zk4/lee'
__download_url__ = '%s/archive/master.zip' % __homepage__
__license__ = 'BSD'

if __name__ == '__main__':
    setup(
        # used in pip install and uninstall 
        # pip install modulename
        name='lee',
        version=__version__,
        author=__author__,
        author_email=__author_email__,
        url=__homepage__,
        description=__description__,
        long_description=open('README.md', 'r', encoding='utf-8').read().strip(),
        long_description_content_type='text/markdown',
        download_url=__download_url__,
        license=__license__,
        python_requires='>3.0.0',
        zip_safe=False,
        packages=find_packages(exclude=['tests', 'tests.*']),
        # package_data={'l': ['py.typed']},
        # data_files=[('', ['logging.yaml'])],  # Optional
        package_data={'lee.logx':['logging.yaml']},
        install_requires=open('requirements.txt', 'r').read().strip().split(),
        entry_points={
            'console_scripts': [
                'lee = lee:entry_point'
            ]
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console'
        ],
        keywords=(
            'best practice for python project'
        )
    )
