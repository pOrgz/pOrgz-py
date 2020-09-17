# -*- encoding: utf-8 -*-

import glob
import json
import time
import sqlite3
import datetime

from abc import ABCMeta

from ..commons.SQLite3 import (
        # Get SQLite Statements to Create Required Tables
        AccountDetails,
        AccountStatements,
        # MobileWallets
    )

from .config import defaults
from ._decorator import initializer
from ..exceptions import InvalidFileFormat

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

    :type  session: dict or JSON
    :param session: The Session Objects holds Information about the User - as available
                    from :func:`pOrgz.userInfo()`. If the file already exists, then fetch
                    if from the file, else prompt user for the information, store it into
                    the file.

    :raises InvalidFileFormat: Mainly raised, if an invalid JSON file is obtained due to
                               :func:`json.JSONDecodeError` while parsing JSON File/Object
    :raises ValueError: If this is raised - then you are advised to raise an Issue with the
                        details, as a fallback mechanism is raised while defining defaults.
    """

    def __init__(self, username : str):
        self.username = username

        # Constants
        self.userDir  = defaults('base_dir')
        self.userfile = defaults('base_file')
        self.database = os.path.join(self.userDir, f'{self.username}.db')

        # Check User Information, and Create Account
        if not os.path.exists(self.userDir): # then create DB and PATH
            os.mkdir(self.userDir)

        if self.conStatus: # able to Create DataBase
            try:
                with open(self.userfile) as f:
                    self.session = json.load(f)[self.username]
            except (KeyError, FileNotFoundError): # Path Exists, but a New User or First-Run
                self.session = self.userInfo()
            except json.JSONDecodeError as err:
                raise InvalidFileFormat(f'Invalid File-Format Found: Please Remove or Correct {self.userfile}')

    def userInfo(self):
        """A Special Function, which Registers a New User
        
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

        _risk  = float(input(f"Risk Factor (0 - 1) [{_defRisk}]:") or _defRisk)
        if (_risk > 1) or (_risk < 0):
            raise ValueError(f'Risk Factor should be between 0 and 1, got {_risk}')

        _capital = float(input('Capital Amount (monthly intake) [10000.00]: ') or '10000')

        if not os.path.exists(self.userfile):
            values = {
                "ID"          : int(time.time()),
                "first_name"  : _fName,
                "middle_name" : _mName,
                "last_name"   : _lName,
                "age"         : _age,
                "risk"        : _risk,
                "captial"     : _capital
            }
            with open(self.userfile, 'w') as f:
                json.dump({self.username : values}, f, indent = 4)

        return values

    @property
    def conStatus(self) -> bool:
        """Checks the Connection Status

        If the database is available in the default path, then checks if it can be
        connected, else if there is no such path then creates a database and tries to connect.
        If the path does not exists, then it creates the path and then builds all the tables from template.

        :rtype:  bool
        :return: `True` if connection was successful, `False` otherwise
        """

        if os.path.exists(self.database):
            create_table = False
        else:
            create_table = True

        con = sqlite3.connect(self.database) # no need of try-catch

        # Create all Required Tables: Only One Query can be Executed at a Time
        if create_table:
            for query in [AccountDetails, AccountStatements]:
                con.execute(query)
        
        con.close() # Close DB File
        return True

    def _defaultRisk_byAge(self, param : int) -> int:
        """Default Risk Values, based on Age"""

        return {
            30 : lambda : 0.85,
            40 : lambda : 0.60
        }.get(param, lambda : 0.45)()

class AccountInformation(metaclass = ABCMeta):
    """An Abstract Base Class of a User's Account, which has
    the following Attributes associated:

    :type  AccountNumber: int: Unique
    :param AccountNumber: Account Number which is typically 10+ digits Long
                          A user can have multiple account, which are all identified
                          by this unique number. Since SQLite3 are built with dynamic
                          typing, thus :py:attr:`~_is_exists` checks if the account already
                          exists.

    :type  ACHolderName: str
    :param ACHolderName: Name of the Account Holder, which is auto-included (by Default)
                         from the information stored in `users.json`

    :type  ACType: str
    :param ACType: Type of the Account, which are as follows:

                   - savings: Savings Account (default)
                   - credit : Credit Card Account
                   - wallet : Signifies Mobile Wallet Accounts

                   It is important to provide an account type, as it signifies
                   critical informations - required for predictive analysis.
                   Simply speaking: **Credit** in a savings account is `+` in analysis
                   and the total monthly **Debit** in credit account should be equal
                   to the credit amount.

    :type  IFSCCode: str
    :param IFSCCode: IFSC Code of the Account (optional, default None)

    :type  CIFNumber: str
    :param CIFNumber: CIF Number of the Account (optional, default None)

    :type  ACOpenDate: str
    :param ACOpenDate: Date on which the account was created.

    :type  ACCloseDate: str
    :param ACCloseDate: Date on which the account is closed, defaults to None

    :type  ContactEmail: str
    :param ContactEmail: Email ID Associated with the account, defaults to None

    :type  ContactMobile: int
    :param ContactMobile: Mobile No. Associated with the account. This is required field.

    :type  BankName: str
    :param BankName: Name of the Bank where the Account was Created

    :type  BranchName: str
    :param BranchName: Branch Name of the Account, defaults to None

    :type  CardNumber: str
    :param CardNumber: 15/16-Digit Card Number Associated with the Account, defaults to None
    """

    # @initializer
    def __init__(
            self,
            AccountNumber : int,
            ACHolderName  : str,
            ACOpenDate    : datetime.datetime,
            ContactMobile : int,
            BankName      : str,
            ACType        : str = 'savings',
            IFSCCode      : str = None,
            CIFNumber     : str = None,
            ACCloseDate   : datetime.datetime = None,
            ContactEmail  : str = None,
            BranchName    : str = None,
            CardNumber    : str = None,
            *args,
            **kwargs
        ):
        pass