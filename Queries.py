def SelectMaxID():
    return "SELECT Elem_ID FROM QUEUE ORDER BY Elem_ID DESC LIMIT 1"


def SelectCurrentCard(card):
    return "SELECT Elem_ID FROM QUEUE WHERE PACS_ID = '" + card + "'"


def Insert2Queue(id, card):
    return "INSERT INTO QUEUE (Elem_ID, PACS_ID) values ('" + str(id) + "', '" + card + "')"


def SelectTodayOrder(date, card):
    return "SELECT Order_ID FROM ORDER_LIST, EMPLOYEE_LIST WHERE EMPLOYEE_LIST.Emp_ID = ORDER_LIST.Employee_ID AND Date = '" + date + "' AND PACS_ID = '" + card + "'"
