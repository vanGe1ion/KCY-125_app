import serial
import json


class SerialListener:
    __portName = None
    __serialPort = None

    def __init__(self, conf_file=None):
        if conf_file is not None:
            try:
                with open(conf_file, "r") as read_file:
                    db_config = json.load(read_file)
                    self.Initialize(db_config['portName'])
                    self.Connect()

            except FileNotFoundError:
                print("\n\rFile error!\n\rFile " + conf_file + " not found\n\r")
                input()
                exit(3)


    def Initialize(self, portName):
        self.__portName = portName

    def Connect(self):
        try:
            print("Connecting to device...")
            self.__serialPort = serial.Serial(self.__portName)
            print("Connected to: " + self.__serialPort.portstr + "\n\r")
        except serial.serialutil.SerialException:
            self.ThrowError("dnf")

    def __del__(self):
        if self.__serialPort is not None:
            print("Closing port " + self.__portName + "\n\r")

    def ReadCard(self):
        try:
            result = str(self.__serialPort.readline())[3:15]
            return result
        except serial.serialutil.SerialException:
            self.ThrowError("disconn")


    def ThrowError(self, type):
        if type == "dnf":
            print("\n\rSerial Port error!\n\rUnable to open serial port " + self.__portName + ". Device not found\n\r")
        elif type == "disconn":
            print("\n\rConnection with device on serial port " + self.__portName + " was lost\n\r")
        input()
        exit(1)
