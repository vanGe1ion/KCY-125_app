import hashlib


def IDCardAdapter (readedString):
    return readedString[3:15]


def DBErrorMessageHandler(code, card):
    incognito = Incognitor(card, 3)

    if code == 1452:
        messType = "Error"
        message = incognito + " card isn't identified"
    elif code == 1062:
        messType = "Warning"
        message = incognito + " card already in queue"
    elif code == 9001:
        messType = "Warning"
        message = "There are no orders for " + incognito + " cardholder today"
    else:
        messType = "Error"
        message = "Unexpected error with " + incognito + " card!"

    return "    " + messType + "! Code " + str(code) + ":\n\r    " + message + "\n\r"


def Incognitor(card, visible):
    length = len(card)
    incognito = ""
    fin = ""

    for x in range(visible):
        if x < length:
            fin = card[length - (x + 1)] + fin
    for x in range(length - visible):
        incognito += "*"
    return incognito + fin


def GetMD5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def GetPersonData(data):
    if data["PACS_ID"] is None:
        pacs = "NULL"
    else:
        pacs = data["PACS_ID"]
    print("\r\n    Person info:\n\r" +
          "    =========================================================\n\r" +
          "\tID: \t\t" + str(data["Emp_ID"]) + "\n\r" +
          "\tFullname: \t" + data["Fullname"] + "\n\r" +
          "\tCard ID: \t" + pacs + "\n\r" +
          "    =========================================================\n\r"
          )


def GetPersonList(data):
    print("\n\r\n\r\n\r    Person list includes " + str(len(data)) + " entries:")
    print("    =========================================================")
    print("    Person %+33s %+15s" % ("Fullname", "Card ID"))
    print("    =========================================================")

    for x in data:
        if x["PACS_ID"] is None:
            pacs = "NULL"
        else:
            pacs = x["PACS_ID"]
        print("\t" + str(x["Emp_ID"]) + "%+35s %+15s" % (x["Fullname"], pacs))

    print("    =========================================================\n\r")

