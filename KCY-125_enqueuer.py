import datetime

import pymysql.err as dbException

from DBConnector import DBConnector
from SerialListener import SerialListener
from Queries import *
from FunctionHub import *

print("\n\r    Initialisation...\n\r")
print("    ---------------------------------------------------------")

configFile = "config.json"
kcy125 = SerialListener(configFile)
database = DBConnector(configFile)

print("    Initialisation finished!\n\r")

while True:
    print("\n\r\n\r\n\r    Person handling...")
    print("    ---------------------------------------------------------")
    print("    Press card...\n\r")
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

                print("    The " + Incognitor(card, 3) + " cardholder was enqueued\n\r")
                card = ""
            except dbException.IntegrityError as error:
                if card != "":
                    code = error.args[0]
                    database.ThrowError(DBErrorMessageHandler(code, card))
