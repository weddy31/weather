import sys
import requests
import json
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        req = requests.get('http://localhost:8080/data')
        soup = BeautifulSoup(req.content, 'html.parser')
        self.data = json.loads(soup.text)
        nazwa_stacji = [self.data[i]['stacja'] for i in range(len(self.data))]
        
        self.temperatura = []
        self.cisnienie = []
        print(self.cisnienie, self.temperatura)

        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 290, 200, 150))
        self.label.setObjectName("label")
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(330, 140, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(nazwa_stacji)  
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 80, 101, 21))
        self.label_2.setObjectName("label_2")
        
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(295,230,160,30)
        self.button.clicked.connect(self.OutputData)
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Output:"))
        self.label_2.setText(_translate("MainWindow", "Wybierz miasto:"))
        self.button.setText(_translate("MainWindow", "Wcisnij, aby zobaczyc pogode"))
    def OutputData(self):
        self.selected_city = self.comboBox.currentText()
        
        self.temperatura.clear()
        self.cisnienie.clear()
        
        for i in self.data:
            if i['stacja'] == self.selected_city:
                self.temperatura.append(i['temperatura'])
                self.cisnienie.append(i['cisnienie'])
                break
        self.temperatura_str = ', '.join(str(temp) for temp in self.temperatura)
        self.cisnienie_str = ', '.join(str(temp) for temp in self.cisnienie)
    
        self.label.setText(self.selected_city + '<br>' + f"temperatura: {self.temperatura_str}\N{DEGREE SIGN}C" + '<br>' + f'cisnienie: {self.cisnienie_str} hPa' )
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
