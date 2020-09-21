#!/usr/bin/env python
# -*- encoding: utf-8 -*-

### --- IF REQUIRED - ADD LICENSING INFORMATION (HERE) --- ###

import os
from setuptools import setup
from setuptools import find_packages

PKG = "pOrgz" # Edit with your package name

# Version File Implementation: https://stackoverflow.com/a/7071358
VERSIONFILE = os.path.join(PKG, 'VERSION')
try:
	VERSION = open(VERSIONFILE, 'rt').read() # always read as str()
except FileNotFoundError as err:
	raise RuntimeError(f'is PKG = {PKG} correctly defined? {err}')

with open("LongDescription.md", "r") as fh:
	long_description = fh.read()

setup(
		name         = PKG,
		version      = VERSION,
		author       = "Debmalya Pramanik",
		author_email = "",

		description                   = "A Financial Organizer and Predictor",
		long_description              = long_description,
		long_description_content_type = "text/markdown",

		url         = "https://github.com/pOrgz/pOrgz-py",
		packages    = find_packages(),
		classifiers = [
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License" # Change as Required
		],
		python_requires  = ">=3.6",  # Specify Requirement
		install_requires = ['numpy'] # Add/Edit as Required
	)