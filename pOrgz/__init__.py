# -*- encoding: utf-8 -*-

__author__    = 'Debmalya Pramanik'
__copyright__ = f"Copyright (c) [year] {__author__}"

# __status__    = ""
# __docformat__ = ""

# Let's Check for the Dependencies
hardDependencies    = ['numpy'] # remove/update from setup.py
# mysql.connector is currently not required, but in subsequent future update this will be required.
missingDependencies = []

for dependency in hardDependencies:
	try:
		__import__(dependency)
	except ImportError:
		missingDependencies.append(dependency)

if missingDependencies:
	raise ImportError('Required Dependencies {}'.format(missingDependencies))

# init-time Option Registrations
from .api import *