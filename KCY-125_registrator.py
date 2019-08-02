import pymysql.err as dbException
import getpass

from DBConnector import DBConnector
from SerialListener import SerialListener
from Queries import *
from FunctionHub import *


print("\n\r\n\r\n\r    Initialisation...")
print("    ---------------------------------------------------------")
configFile = "config.json"
kcy125 = SerialListener(configFile)
database = DBConnector(configFile)
print("    Initialisation finished!")


print("\n\r\n\r\n\r    Admin authorisation...")
print("    ---------------------------------------------------------")
logging = 1
while logging:
    adminLogin = input("    Login: ")
    adminPass = GetMD5(getpass.getpass('    Password: '))

    queryResult = database.QueryExecute(SelectAuthorisation(adminLogin, adminPass))
    if queryResult is 0:
        print("\n\r    User with such login and password does not exist\n\r")
        print("    ---------------------------------------------------------")
    else:
        authData = database.QueryResult()[0]
        if authData['Access_ID'] is not 0:
            print("\n\r    User '" + adminLogin + "' does not have the administrator's rights\n\r")
            print("    ---------------------------------------------------------")
        else:
            print("\n\r    Logged in as '" + adminLogin + "'")
            logging = 0


while True:
    database.Necromancy()

    queryResult = database.QueryExecute(SelectEmployees())
    GetPersonList(database.QueryResult())

    print("\n\r\n\r\n\r    Person handling...")
    print("    ---------------------------------------------------------")

    try:
        person = int(input("    Press the person ID: "))
    except ValueError:
        input("\n\r    The person ID can be a decimal integer only!")
        continue

    queryResult = database.QueryExecute(SelectEmployeeData(person))
    if queryResult is 0:
        input("\n\r    Person not found\n\r")
    else:
        personData = database.QueryResult()[0]
        GetPersonData(personData)
        if personData["PACS_ID"] is not None:
            question = ""
            while question is not "y" and question is not "n":
                question = input("    Personal card ID already assigned. Replace? (y/n): ")
            if question is "n":
                continue

        print("    Press card...")
        card = IDCardAdapter(kcy125.SerialRead())
        if card is "":
            kcy125.ThrowError("disconn")
        else:
            print("    Card ID: " + card + "\n\r")

            queryResult = database.QueryExecute(SelectEmpByPACS(card))
            if queryResult is 1:
                res = database.QueryResult()[0]
                input("\n\r    ID card already in use by \n\r    " + res["Fullname"] + " (person ID: " + str(res["Emp_ID"]) + ")\n\r")
            else:
                try:
                    print("    Updating...")
                    database.QueryExecute(UpdatePACS(person, card))
                    database.QueryCommit()
                    input("    Card ID assigned to current person (ID:" + str(person) + ")\n\r")
                except dbException.IntegrityError as error:
                    if card != "":
                        code = error.args[0]
                        database.ThrowError(DBErrorMessageHandler(code, card))

