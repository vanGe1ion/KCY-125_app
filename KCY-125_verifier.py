import datetime

import pymysql.err as dbException

from DBConnector import DBConnector
from SerialListener import SerialListener
from Queries import *
from FunctionHub import *

print("\n\r")

configFile = "config.json"
kcy125 = SerialListener(configFile)
database = DBConnector(configFile)

print("    Ready!\n\r")

while True:
    card = IDCardAdapter(kcy125.SerialRead())
    database.Necromancy()

    queryResult = database.QueryExecute(SelectCurrentCard(card))
    if queryResult:
        database.ThrowError(DBErrorMessageHandler(1062, card))
    else:
        queryResult = database.QueryExecute(SelectTodayOrder(str(datetime.date.today()), card))
        if queryResult is 0:
            database.ThrowError(DBErrorMessageHandler(9001, card))
        else:
            queryResult = database.QueryExecute(SelectMaxID())

            if queryResult:
                result = int(database.QueryResult()[0]['Elem_ID'])
                newID = result + 1
            else:
                newID = 1

            try:
                database.QueryExecute(Insert2Queue(newID, card))
                database.QueryCommit()

                print("    ID card " + Incognitor(card, 3) + " was handled\n\r")
                card = ""
            except dbException.IntegrityError as error:
                if card != "":
                    code = error.args[0]
                    database.ThrowError(DBErrorMessageHandler(code, card))
