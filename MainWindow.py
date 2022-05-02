from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QWidget
from FaceRecognition import Face
import numpy
import os
import sys

class Ui_MainWindow(QWidget):
    filename = None
    url = None
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(772, 753)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.imageToFind = QtWidgets.QLabel(self.centralwidget)
        self.imageToFind.setText("")
        self.imageToFind.setPixmap(QtGui.QPixmap("E:\\Kuliah\\Semester 4\\KB\\yourimagehere.png"))
        self.imageToFind.setScaledContents(True)
        self.imageToFind.setAlignment(QtCore.Qt.AlignCenter)
        self.imageToFind.setWordWrap(False)
        self.imageToFind.setObjectName("imageToFind")
        self.gridLayout.addWidget(self.imageToFind, 0, 0, 2, 2)
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setObjectName("uploadButton")
        self.gridLayout.addWidget(self.uploadButton, 2, 0, 1, 1)
        self.detectButton = QtWidgets.QPushButton(self.centralwidget)
        self.detectButton.setEnabled(False)
        self.detectButton.setObjectName("detectButton")
        self.gridLayout.addWidget(self.detectButton, 2, 1, 1, 1)
        self.output = QtWidgets.QLabel(self.centralwidget)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 3, 0, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 4, 0, 1, 2)
        self.addNewPerson = QtWidgets.QPushButton(self.centralwidget)
        self.addNewPerson.setEnabled(False)
        self.addNewPerson.setObjectName("addNewPerson")
        self.gridLayout.addWidget(self.addNewPerson, 4, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.uploadButton.clicked.connect(self.openFileNameDialog)
        self.detectButton.clicked.connect(self.detectFace)
        self.addNewPerson.clicked.connect(self.confirmAdd)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        
    def openFileNameDialog(self):
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        self.filename = fileName
        if fileName:
            print(fileName)
            imagePixmap = QtGui.QPixmap(fileName)
            imagePixmap = imagePixmap.scaled(800,600,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
            self.imageToFind.setPixmap(imagePixmap)
            self.detectButton.setDisabled(False)
            self.url = fileName
            
    def confirmAdd(self):
        listPeople = os.listdir("KnownImages")
        personName = self.lineEdit.text()
        self.newFace.name = personName
        print(listPeople)
        print(personName)
        if not personName in listPeople:    
            self.createNewPerson()
            self.output.setText(personName + " has been Added!")
            self.lineEdit.setDisabled(True)
            self.lineEdit.setText("")
            self.addNewPerson.setDisabled(True)

    def saveFace(self):
        listFiles = os.listdir("KnownImages/" + self.newFace.name)
        if(len(listFiles) <= 3):
            numpy.save("KnownImages/"+ self.newFace.name+ "/" + self.newFace.name + str(len(listFiles) + 1),self.newFace.encoding)

        
        
    def createNewPerson(self):
        os.mkdir("KnownImages/" + self.newFace.name)
        listFiles = os.listdir("KnownImages/" + self.newFace.name)
        numpy.save("KnownImages/"+ self.newFace.name+ "/" + self.newFace.name + str(len(listFiles) + 1),self.newFace.encoding)

            
    def detectFace(self):
        self.newFace = Face("",self.filename)
        name = self.newFace.findPerson()
        _translate = QtCore.QCoreApplication.translate
        if name != "Unknown":
            self.output.setText(_translate("MainWindow","This is " + name))
            self.saveFace()
        elif name == "Unknown":
            self.output.setText(_translate("MainWindow","Person Unknown \nClick button below to add new person"))
            self.addNewPerson.setDisabled(False)
            self.lineEdit.setDisabled(False)
        self.detectButton.setDisabled(True)

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Recognition"))
        self.uploadButton.setText(_translate("MainWindow", "Choose File"))
        self.detectButton.setText(_translate("MainWindow", "Detect Face"))
        self.output.setText(_translate("MainWindow", "Person Name"))
        self.addNewPerson.setText(_translate("MainWindow", "Add"))
        

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



