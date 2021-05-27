# Konrad Budukiewicz, Tomasz Czajkowski
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtGui
import sys
import random


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.setWindowIcon(QtGui.QIcon('295128.png'))
        self.setWindowTitle('Logowanie')
        self.text_name = QLineEdit(self)
        self.text_pass = QLineEdit(self)

        self.button_login = QPushButton('Zaloguj', self)
        self.button_login.clicked.connect(self.handle_login)

        layout = QVBoxLayout(self)

        layout.addWidget(self.text_name)
        layout.addWidget(self.text_pass)
        layout.addWidget(self.button_login)

    def handle_login(self):
        if (self.text_name.text() == 'user' and self.text_pass.text() == 'pass'):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Linia produkcyjna')
        self.setWindowIcon(QtGui.QIcon('istockphoto-1015371622-612x612.jpg'))
        self.setFixedSize(451, 534)

        self.activity_label = QLabel(self)
        self.activity_label.setGeometry(250, 375, 150, 105)

        self.timer_activity = QTimer(self)
        self.timer_activity.timeout.connect(self.couting)

        self.timer_proccesor = QTimer(self)
        self.timer_proccesor.timeout.connect(self.simulation)

        self.bar1 = QProgressBar(self)
        self.bar1.setGeometry(240, 120, 171, 31)

        self.bar2 = QProgressBar(self)
        self.bar2.setGeometry(240, 170, 171, 31)

        self.bar3 = QProgressBar(self)
        self.bar3.setGeometry(240, 220, 171, 31)

        self.label1 = QLabel(self)
        self.label1.setGeometry(30, 120, 201, 16)
        self.label1.setText('Temperatura CPU:')

        self.label2 = QLabel(self)
        self.label2.setGeometry(30, 170, 201, 16)
        self.label2.setText('Uzycie CPU:')

        self.label3 = QLabel(self)
        self.label3.setGeometry(30, 220, 201, 16)
        self.label3.setText('Uzycie wentylatorow:')

        self.label4 = QLabel(self)
        self.label4.setGeometry(100, 310, 201, 16)

        self.label5 = QLabel(self)
        self.label5.setGeometry(100, 270, 201, 16)

        self.label6 = QLabel(self)
        self.label6.setGeometry(100, 350, 201, 16)

        self.label7 = QLabel(self)
        self.label7.setGeometry(40, 390, 201, 16)
        self.label7.setText('Aktywnosc uzytkownika')

        self.label8 = QLabel(self)
        self.label8.setGeometry(40, 420, 201, 16)
        self.label8.setText('Uzytkownik ma czas na dzialanie:')

        self.start = QPushButton('Start produkcji', self)
        self.start.setGeometry(50, 40, 171, 41)
        self.start.clicked.connect(self.start_production)

        self.end = QPushButton('Stop produkcji', self)
        self.end.setGeometry(240, 40, 171, 41)
        self.end.clicked.connect(lambda: self.close())

        self.action = QPushButton('Potwierdz aktywnosc', self)
        self.action.setGeometry(40, 450, 171, 41)
        self.action.clicked.connect(self.show_action)

        self.show()

    def start_production(self):
        self.time = 30
        self.timer_proccesor.start(1000)
        self.timer_activity.start(1000)

    def couting(self):
        self.time -= 1
        list_time1 = [1, 3, 5, 7, 9]
        list_time2 = [2, 4, 6, 8, 10]
        self.activity_label.setText(f'00:{self.time}')
        if self.time == 0:
            self.timer_activity.stop()
        elif self.time in list_time1:
            self.setStyleSheet("background-color: yellow;")
        elif self.time in list_time2:
            self.setStyleSheet("background-color: white;")
        if self.time == 0:
            self.close()

    def show_action(self):
        self.time = 30
        self.timer_activity.start()

    def simulation(self):
        self.proc_usage = random.randint(10, 95)
        self.proc_temp = self.proc_usage - 5
        self.vents = 25
        if self.proc_temp < 25:
            self.bar3.setValue(self.vents)
            self.bar3.setStyleSheet("QProgressBar::chunk ""{""background-color: green;""}")
            self.label4.setText('Temperatura: W NORMIE')
            self.label5.setText('Wlaczono 1 wentylator')
            self.label6.setText('Uzycie procesora: MINIMALNE')
            self.proc_temp = self.proc_temp - 10
        elif 50 > self.proc_temp >= 25:
            self.vents = 2 * self.vents
            self.bar3.setValue(self.vents)
            self.bar3.setStyleSheet("QProgressBar::chunk ""{""background-color: yellow;""}")
            self.label4.setText('Temperatura: MALA')
            self.label5.setText('Wlaczono 2 wentylatory')
            self.label6.setText('Uzycie procesora: W NORMIE')
            self.proc_temp = self.proc_temp - 20
        elif 75 > self.proc_temp >= 50:
            self.vents = 3 * self.vents
            self.bar3.setValue(self.vents)
            self.bar3.setStyleSheet("QProgressBar::chunk ""{""background-color: orange;""}")
            self.label4.setText('Temperatura: ZA DUZA')
            self.label5.setText('Wlaczono 3 wentylatory')
            self.label6.setText('Uzycie procesora: DUZE')
            self.proc_temp = self.proc_temp - 30
        else:
            self.vents = 4 * self.vents
            self.bar3.setValue(self.vents)
            self.bar3.setStyleSheet("QProgressBar::chunk ""{""background-color: red;""}")
            self.label4.setText('Temperatura: DUZA')
            self.label5.setText('Wlaczono 4 wentylatory')
            self.label6.setText('Uzycie procesora: BARDZO DUZE')
            self.proc_temp = self.proc_temp - 40

        self.bar1.setValue(self.proc_temp)
        self.bar2.setValue(self.proc_usage)

        if self.proc_usage > 80 and self.proc_temp > 70:
            self.bar1.setStyleSheet("QProgressBar::chunk ""{""background-color: red;""}")
            self.bar2.setStyleSheet("QProgressBar::chunk ""{""background-color: red;""}")
        elif self.proc_usage < 50 and self.proc_temp < 50:
            self.bar1.setStyleSheet("QProgressBar::chunk ""{""background-color: green;""}")
            self.bar2.setStyleSheet("QProgressBar::chunk ""{""background-color: green;""}")
        else:
            self.bar1.setStyleSheet("QProgressBar::chunk ""{""background-color: yellow;""}")
            self.bar2.setStyleSheet("QProgressBar::chunk ""{""background-color: yellow;""}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = MyWindow()
        window.show()
        sys.exit(app.exec_())