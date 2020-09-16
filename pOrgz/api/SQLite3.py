# -*- encoding: utf-8 -*-

"""Contains SQLite3 Query used for Various Purposes"""

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
    `CardNumber`    bigint      NOT NULL ,

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

MobileWallets = """
CREATE TABLE `MobileWallets` (
    `WalletID`   varchar(45) NOT NULL ,
    `WName`      varchar(45) NOT NULL ,
    `WOpenDate`  date        NOT NULL ,
    `WCloseDate` date        NULL ,
    `WLimit`     numeric     NOT NULL ,

    PRIMARY KEY (`WalletID`)
);"""