# -*- encoding: utf-8 -*-

"""Global Level Configurations and Parameters are Defined"""

import os
import glob
import json
import time
import sqlite3

class pOrgz:
    """A Core Class for Initializing and Defining Options for pOrgz

    A new/existing user will reside in ``.users`` directory for and :class:`pOrgz.pOrgz` to work,
    if the directory does not exists then a directory of the same name is created by default.
    Once the directory is created, all individual user have their own database, where
    the name of the user is the name of the database which contains all the files.

    Currently, all the information is stored in an unencrypted DB (provided by ``SQLite3``),
    but later, this should be moved to a secure database, or an encryption policy will be set.
    
    :param username: as :mod:`pOrgz` supports multi-user, this looks for the username in
                     the directory ``.users``, if not found then it invokes necessary commands
                     to create the database and all the associated tables.
                     This function should later be used by RestAPI, when integrated with GUI.

    :type  userDir: str: const
    :param userDir: Directory where all the database are stored, which is ``.users``

    :type  database: str: const
    :param database: Name of the database, which is ``.users/username.db``

    :type  userfile: str: const
    :param userfile: Name of the File where all the users information is stored.
                     This file is created and invoked from :func:`pOrgz.userInfo()`
                     and a JSON structure is created.
    """

    def __init__(self, username : str):
        self.username = username

        # Constants
        self.userDir  = os.path.join('.', '.users')
        self.userfile = os.path.join(self.userDir, 'users.json')
        self.database = os.path.join(self.userDir, f'{self.username}.db')

    def userInfo(self):
        """A Special Function, which stores the user informations
        
        A special file ``users.json`` keeps tracks of all the user informations,
        if the user does not exists, then this function is automatically triggered and
        the file is updated accordingly. Apart from this, it also checks if
        the number of keys i.e. user count is same as that of the database created.
        In the following questions, if marked with a ``*`` then the value is advised,
        while others are optional. If any has a default value, then it is mentioned in
        square brackets.

        :type  ID: int
        :param ID: An Unique ID Associated with the User, automatically generated.

        :type  first_name: str
        :param first_name: First Name of the User

        :type  middle_name: str
        :param middle_name: Middile Name of the User

        :type  last_name: str
        :param last_name: Middile Name of the User

        :type  age: float
        :param age: Age of the User

        :type  risk: float
        :param risk: Based on the age of the user, a default risk is associated. Default Risk Values
                     - based on the User's Age, are
                     If ``age < 30 : risk = 85%`` elseif ``age < 40 : risk = 60%`` else ``risk = 45%``
                     The value of the risk is between 0 to 1, example:
                     ``risk = 0.9 = 90%`` signifies the user is ready to invest 90% of its capital
                     into risky-investements like stocks.

        :type  captial: float
        :param capital: Capital Amount, i.e. the monthly intake of the user (from all sources).
                        Initially, it is advised that the user provides some values. However,
                        efficient algorithms should be able to gather this amount.
                        Default ₹ 10, 000.00 /-
        """

        if not os.path.exists(self.userfile):
            try:
                values = self._getUserInfo()

                with open(self.userfile, 'w') as file_:
                    json.dump({self.username : values}, file_)

            except PermissionError as err:
                raise PermissionError(f'Unable to create necessary file: {self.userfile}', err)

    @property
    def conStatus(self) -> bool:
        """Checks the Connection Status

        If the database is available in the default path, then checks if it can be
        connected, else if there is no such path then creates a database and tries to connect.
        If the path does not exists, then it creates the path and then builds all the tables from template.

        :rtype:  bool
        :return: `True` if connection was successful, `False` otherwise

        :raises PermissionError: if unable to create directory
        """

        if not os.path.exists(self.userDir):
            try:
                os.mkdir(self.userDir)
            except PermissionError as err:
                raise PermissionError(f'Unable to directory: {self.userDir}', err)

        connection = sqlite3.connect(self.database) # no need of try-catch

        return True

    def _getUserInfo(self) -> dict:
        """Asks Questions to Populate the User-Informations"""

        _fName = input("First Name*: ")
        _mName = input("Middle Name: ")
        _lName = input("Last/Family Name*: ")

        _age   = float(input("Age*: ")) # Based on age, define risk

        if _age < 30:
            _defRisk = self._defaultRisk_byAge(30)
        elif _age < 40:
            _defRisk = self._defaultRisk_byAge(40)
        else:
            _defRisk = 0.45

        _risk  = float(input(f"Risk Factor (0 - 1) [{_defRisk}]:"))
        if (_risk > 1) or (_risk < 0):
            raise ValueError(f'Risk Factor should be between 0 and 1, got {_risk}')

        _capital = float(input('Capital Amount (monthly intake) [10000.00]: ') or '10000')

        return {
            "ID"          : int(time.time()),
            "first_name"  : _fName,
            "middle_name" : _mName,
            "last_name"   : _lName,
            "age"         : _age,
            "risk"        : _risk,
            "captial"     : _capital
        }

    def _defaultRisk_byAge(self, param : int) -> int:
        """Default Risk Values, based on Age"""

        return {
            30 : lambda : 0.85,
            40 : lambda : 0.60
        }.get(param, lambda : 0.45)()