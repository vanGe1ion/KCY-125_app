def SelectMaxID():
    return "SELECT Elem_ID FROM QUEUE DIST LIMIT 1"

def SelectCurrentCard(card):
    return "SELECT Elem_ID FROM QUEUE WHERE PACS_ID = '" + card + "'"

def Insert2Queue(id, card):
    return "INSERT INTO QUEUE (Elem_ID, PACS_ID) values ('" + str(id) + "', '" + card + "')"

