# -*- encoding: utf-8 -*-

"""Currently, the functionalities are being checked,
for which these module are built to provide basic functionalities.
"""

import sqlite3
import pandas as pd

def _insert_data_into_account_statements(data : pd.DataFrame, base_obj, include_account = True, account_number = None):
    """Insert Data into Account Statement Table Created in SQLite3"""

    data = data.copy() # copy the data within function - to preserve the original data
    con = sqlite3.connect(base_obj.database)

    if include_account:
        data['AccountNumber'] = account_number

    data.rename(columns = {
            'Txn Date'           : 'TXNDate',
            'Value Date'         : 'ValueDate',
            'Ref No./Cheque No.' : 'Remarks',
            ' Debit'             : 'Debit' # I've no Idea why there is a Space -_-
        }, inplace = True)

    data.to_sql('AccountStatements', con, if_exists = 'append', index = False)

    con.close()
    return True