# -*- encoding: utf-8 -*-

"""Configuration of Default Path, Files and Directories"""

import os

def defaults(param : str) -> str:
    # use the param to get the default values
    # RECOMENDED: Not to Change the Directory
    return {
        'base_dir'  : lambda : os.path.join('.', '.users'),
        'base_file' : lambda : os.path.join(self.userDir, 'users.json')
    }.get(param, lambda : (_ for _ in ()).throw(ValueError(f'{param} is not Valid: Please Raise an Issue')))()