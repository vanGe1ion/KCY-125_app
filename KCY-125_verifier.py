import pymysql.err as dbException

from DBConnector import DBConnector
from SerialListener import SerialListener
from Queries import *

configFile = "config.json"

kcy125 = SerialListener(configFile)
dbConnector = DBConnector(configFile)


while True:
    card = kcy125.ReadCard()

    dbConnector.Necromancy()
    selectRes = dbConnector.QueryExecute(SelectCurrentCard(card))
    if selectRes:
        dbConnector.ThrowError(1062)
    else:
        selectRes = dbConnector.QueryExecute(SelectMaxID())

        if selectRes:
            result = int(dbConnector.QueryResult()[0]['Elem_ID'])
            newID = result + 1
        else:
            newID = 1

        try:
            dbConnector.QueryExecute(Insert2Queue(newID, card))
            dbConnector.QueryCommit()

            length = len(card)
            fin = card[length-3]+card[length-2]+card[length-1]
            incognito = ""
            for x in range(length-3):
                incognito += "*"

            print("ID card " + incognito + fin + " was handled\n\r")
            card = ""
        except dbException.IntegrityError as error:
            if card != "":
                code, message = error.args
                dbConnector.ThrowError(code)
