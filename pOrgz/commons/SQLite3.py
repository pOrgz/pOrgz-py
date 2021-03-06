# -*- encoding: utf-8 -*-

"""Contains SQLite3 Query used for Various Purposes

NOTE: SQLite3 does not check for Data-Types while inserting data, as it supports
Dynamic Typing: https://sqlite.org/faq.html#q3

Thus, all the types and key bindings are not necessary - however it will serve as
hint for data merging later. Also, when encrypted service is enabled, this will be
updated accordingly.

NOTE: This file has to be Removed from Documentations!
"""

AccountDetails = """
CREATE TABLE `AccountDetails` (
    `AccountNumber` bigint      NOT NULL ,
    `ACHolderName`  varchar(45) NOT NULL ,
    `ACType`        varchar(45) NOT NULL ,
    `IFSCCode`      varchar(45) NULL ,
    `CIFNumber`     varchar(45) NULL ,
    `ACOpenDate`    date        NOT NULL ,
    `ACCloseDate`   date        NULL ,
    `ContactEmail`  varchar(45) NULL ,
    `ContactMobile` bigint      NOT NULL ,
    `BankName`      varchar(45) NOT NULL ,
    `BranchName`    varchar(45) NULL ,
    `CardNumber`    bigint      NULL ,

    PRIMARY KEY (`AccountNumber`)
);"""

AccountStatements = """
CREATE TABLE `AccountStatements` (
    `AccountNumber` bigint      NOT NULL ,
    'TXNDate'       date        NOT NULL ,
    'ValueDate'     date        NULL ,
    'Description'   varchar(45) NULL ,
    'Remarks'       varchar(45) NULL ,
    'Debit'         numeric     NULL ,
    'Credit'        numeric     NULL ,
    'Balance'       numeric     NOT NULL ,

    CONSTRAINT fk_ACNumber
        FOREIGN KEY (`AccountNumber`)
        REFERENCES 'AccountDetails'(`AccountNumber`)
);"""

# Monthly Statement will later be a sub table of AccountStatements
MonthlyStatement = """
CREATE TABLE `MonthlyStatement` (
    `AccountNumber`  bigint      NOT NULL ,
    'TXNMonth'       date        NOT NULL ,
    'OpeningBalance' numeric     NULL ,

    CONSTRAINT fk_ACNumber
        FOREIGN KEY (`AccountNumber`)
        REFERENCES 'AccountDetails'(`AccountNumber`)
);"""

MobileWallets = """
CREATE TABLE `MobileWallets` (
    `WalletID`   varchar(45) NOT NULL ,
    `WName`      varchar(45) NOT NULL ,
    `WOpenDate`  date        NOT NULL ,
    `WCloseDate` date        NULL ,
    `WLimit`     numeric     NOT NULL ,

    PRIMARY KEY (`WalletID`)
);"""