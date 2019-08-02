def SelectMaxID():
    return "SELECT Elem_ID FROM QUEUE ORDER BY Elem_ID DESC LIMIT 1"


def SelectCurrentCard(card):
    return "SELECT Elem_ID FROM QUEUE WHERE PACS = '" + card + "'"


def Insert2Queue(id, card):
    return "INSERT INTO QUEUE (Elem_ID, PACS) values ('" + str(id) + "', '" + card + "')"


def SelectTodayOrder(date, card):
    return "SELECT Order_ID FROM ORDER_LIST, EMPLOYEE_LIST WHERE EMPLOYEE_LIST.Emp_ID = ORDER_LIST.Employee_ID AND Date = '" + date + "' AND PACS = '" + card + "'"


def SelectAuthorisation(login, passw):
    return "SELECT Profile_ID, Access_ID FROM PROFILE_LIST WHERE Login='" + login + "' AND Password='" + passw + "'"


def SelectEmployeeData(Emp_ID):
    return "SELECT Emp_ID, Fullname, PACS FROM EMPLOYEE_LIST WHERE Emp_ID='" + str(Emp_ID) + "'"


def SelectEmployees():
    return "SELECT Emp_ID, Fullname, PACS FROM EMPLOYEE_LIST"


def SelectEmpByPACS(PACS):
    return "SELECT Emp_ID, Fullname FROM EMPLOYEE_LIST WHERE PACS ='" + PACS + "'"


def UpdatePACS(Emp_ID, PACS):
    return "UPDATE EMPLOYEE_LIST SET PACS = '" + PACS + "' WHERE Emp_ID = '" + str(Emp_ID) + "'"
