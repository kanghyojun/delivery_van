#! -*- coding: utf-8 -*-
from setuptools import setup

setup(name='artist_crawler',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'requests==2.2.1', 'lxml==3.3.3', 'pytest==2.5.2'
      ])