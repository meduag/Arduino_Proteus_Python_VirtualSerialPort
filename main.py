import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import serial.tools.list_ports

__author__ = 'Miguel Gutierrez'

# Original ports
serPort1 = "COM14"  # Stim
baudRate = 2000000


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("terminal1.ui", self)

        # colocar linkado de botones
        self.PB_conectar.clicked.connect(self.connect_to_arduino)
        self.PB_desconectar.clicked.connect(self.desconnect_to_arduino)

        # self.listWidget
        # self.listWidget.addItem(f"Hola") # asi adiciono un puerto al item
        # Listar los puertos disponibles
        self.list_ports()

        # Show interface
        self.show()

    def list_ports(self):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            self.listWidget.addItem(f"Puerto: {port}")

    # @pyqtSlot()
    def connect_to_arduino(self):
        global serPort1
        selected_port = self.listWidget.currentItem().text().split()[1]
        serPort1 = selected_port
        # Aquí puedes utilizar la variable selected_port para conectarte al Arduino
        print("Conectando al puerto", selected_port)
        self.init_serial()
        # Agrega tu código para conectarte al Arduino

    def desconnect_to_arduino(self):
        global serPort1
        serPort1 = self.listWidget.currentItem().text().split()[1]
        ser = serial.Serial()
        ser.close()
        QMessageBox.information(self, "Desconectando", "Puerto " + serPort1 + " desconectado")

    # @static
    def init_serial(self):
        global serPort1
        port = serPort1  # Stim
        baud = 152000

        ser = serial.Serial()
        ser.port = port
        ser.timeout = 1
        ser.baudrate = baud
        ser.xonxoff = 1

        msg_bytes = str.encode("$$")

        try:
            ser.open()
            QMessageBox.information(self, "Conectado", "Puerto " + serPort1 + " conectado")
        except Exception as e:
            print("Error open serial port: " + str(e) + " En -- read_serial --")
            QMessageBox.critical(self, "Error", "¡No se pudo conectar al puerto " + serPort1)
            exit()

        if ser.isOpen():
            try:
                ser.write(msg_bytes)
                print("Start capture for Stim data")
                while 1:
                    c = ser.readline()
                    if len(c) > 0:
                        # time1 = time.time()
                        str_msn = c.decode("utf-8")
                        str_msn = str_msn.rstrip()
                        print(str_msn)
                        # time2 = time.time()
                        # time3 = time2 - time1
                        # print(str(time3))

            except Exception as e1:
                print("Error communicating...: " + str(e1) + " En -- read_serial --")

        else:
            print("Cannot open serial port " + str(port) + " En -- read_serial --")
            exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    '''app.aboutToQuit.connect(exit_program_and_stim)'''
    ex = MainWindow()
    sys.exit(app.exec_())
