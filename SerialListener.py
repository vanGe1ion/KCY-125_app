import serial
import json


class SerialListener:
    __portName = None
    __serialPort = None
    __deviceName = None

    def __init__(self, conf_file=None):
        if conf_file is not None:
            try:
                with open(conf_file, "r") as read_file:
                    db_config = json.load(read_file)
                    self.Initialize(db_config['portName'], db_config['deviceName'])
                    self.Connect()

            except FileNotFoundError:
                print("\n\r    File error!\n\rFile " + conf_file + " not found\n\r")
                input()
                exit(3)

    def Initialize(self, portName, deviceName):
        self.__portName = portName
        self.__deviceName = deviceName

    def Connect(self):
        try:
            print("    Connecting to " + self.__deviceName + " device...")
            self.__serialPort = serial.Serial(self.__portName)
            print("    Connected to " + self.__deviceName + " device on " + self.__serialPort.portstr + " serial port\n\r")
        except serial.serialutil.SerialException:
            self.ThrowError("dnf")

    def __del__(self):
        if self.__serialPort is not None:
            print("    Closing " + self.__portName + " serial port\n\r")

    def SerialRead(self):
        try:
            result = str(self.__serialPort.readline())
            return result
        except serial.serialutil.SerialException:
            self.ThrowError("disconn")

    def ThrowError(self, type):
        if type == "dnf":
            print("\n\r    Serial error!\n\rUnable to open " + self.__portName + " serial port. " + self.__portName + " device not found\n\r")
        elif type == "disconn":
            print("\n\r    Connection with " + self.__deviceName + " device on " + self.__portName + " serial port was lost\n\r")
        input()
        exit(1)
