import json
import pymysql.cursors


class DBConnector:
    __connection = None
    __cursor = None
    __host = None
    __user = None
    __pass = None
    __db = None

    def __init__(self, conf_file=None):
        if conf_file is not None:
            try:
                with open(conf_file, "r") as read_file:
                    db_config = json.load(read_file)

                    self.Initialize(db_config['hostname'],
                                    db_config['user'],
                                    db_config['password'],
                                    db_config['dbname'])

                    self.CreateConnection()
                    self.GetConnectionInfo()
            except FileNotFoundError:
                print("\n\rFile error!\n\rFile " + conf_file + " not found\n\r")
                input()
                exit(3)

    def __del__(self):
        self.CloseConnection()

    def Initialize(self, host, user, passw, db):
        self.__host = host
        self.__user = user
        self.__pass = passw
        self.__db = db

    def CreateConnection(self):
        try:
            print("Connecting to database...")
            self.__connection = pymysql.connect(host=self.__host,
                                                user=self.__user,
                                                password=self.__pass,
                                                db=self.__db,
                                                cursorclass=pymysql.cursors.DictCursor)
            print("Connected to " + self.__db + " database on " + self.__host + "\n\r")
            self.__cursor = self.__connection.cursor()
        except:
            print("Database connection to " + self.__host + " was failed!\n\r")
            input()
            exit(2)

    def CloseConnection(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
            self.__cursor = None
            print("Closing database connection to " + self.__host + "\n\r")

    def GetConnectionInfo(self):
        print("Database connection information\n\r" +
              "=========================================================\n\r" +
              "Host name: " + self.__host + "\n\r" +
              "User name: " + self.__user + "\n\r" +
              "Database name " + self.__db + "\n\r" +
              "=========================================================\n\r"
              )

    def GetCursorDescription(self):
        print("\n\rCurrent cursor scheme:\n\r" +
              "=========================================================")
        for desc in self.__cursor.description:
            print(desc)
        print("=========================================================\n\r")

    def QueryExecute(self, query):
        return self.__cursor.execute(query)

    def QueryResult(self):
        return self.__cursor.fetchall()

    def QueryCommit(self):
        self.__connection.commit()

    def ThrowError(self, code):
        if code == 1452:
            message = "Unknown ID card detected"
        elif code == 1062:
            message = "ID card already in queue"
        else:
            message = "Unexpected error!"

        print("Error! Code " + str(code) + ":\n\r" +
              message + "\n\r")

    def Necromancy(self):
        self.__connection.ping(True)
