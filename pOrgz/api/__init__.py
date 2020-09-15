# -*- encoding: utf-8 -*-

"""Global Level Configurations and Parameters are Defined"""

import os
import sqlite3

class pOrgz:
    """A Core Class for Initializing and Defining Options for pOrgz

    A new/existing user will reside in .users directory for pOrgz to work,
    if the directory does not exists then a directory of the same name is created by default.
    Once the directory is created, all individual user have their own database, where
    the name of the user is the name of the database which contains all the files.

    Currently, all the information is stored in an unencrypted DB (provided by SQLite3),
    but later, this should be moved to a secure database, or an encryption policy will be set.
    
    :param username: as pOrgz supports multi-user, this looks for the username in
                     the directory .users, if not found then it invokes necessary commands
                     to create the database and all the associated tables.
                     This function should later be used by RestAPI, when integrated with GUI.
    """

    def __init__(self, username : str):
        self.username = username

        # Constants
        self.userDir  = os.path.join('.', '.users')
        self.database = os.path.join(self.userDir, f'{self.username}.db')

    @property
    def conStatus(self) -> bool:
        """Checks the Connection Status

        If the database is available in the default (.users) path, then checks if it can be
        connected, else if there is no such path then creates a database and tries to connect.

        Returns:
        :param status: Returns True if available, else raise errors.

        Raises:
        PermissionError : if unable to creater directory and/or database
        """

        if not os.path.exists(self.userDir):
            try:
                os.mkdir(self.userDir)
            except PermissionError as err:
                raise PermissionError(f'Unable to directory: {self.userDir}', err)

        connection = sqlite3.connect(self.database) # no need of try-catch
        return True