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
