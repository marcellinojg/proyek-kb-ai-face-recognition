from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QWidget
from PyQt5.QtCore import (QThread,pyqtSignal)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from cv2 import cvtColor
from sqlalchemy import false
from FaceRecognition import Face
import time
import numpy
import os
import sys
import cv2

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
        self.imageToFind.setPixmap(QtGui.QPixmap("Asset/yourimagehere.png"))
        self.imageToFind.setScaledContents(True)
        self.imageToFind.setAlignment(QtCore.Qt.AlignCenter)
        self.imageToFind.setWordWrap(False)
        self.imageToFind.setObjectName("imageToFind")
        self.gridLayout.addWidget(self.imageToFind, 0, 0, 2, 2)
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setObjectName("uploadButton")
        self.gridLayout.addWidget(self.uploadButton, 2, 0, 1, 1)
        self.cameraButton = QtWidgets.QPushButton(self.centralwidget)
        self.cameraButton.setObjectName("cameraButton")
        self.gridLayout.addWidget(self.cameraButton, 2, 1, 1, 1)
        self.detectButton = QtWidgets.QPushButton(self.centralwidget)
        self.detectButton.setEnabled(False)
        self.detectButton.setObjectName("detectButton")
        self.gridLayout.addWidget(self.detectButton, 2, 2, 1, 1)
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
        self.cameraButton.clicked.connect(self.startCamera)
        self.detectButton.clicked.connect(self.detectFace)
        self.addNewPerson.clicked.connect(self.confirmAdd)
        
        self.cameraWorker = CameraThread()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
    def disableCamera(self):
        _translate = QtCore.QCoreApplication.translate
        if self.cameraWorker:
            if self.cameraWorker.ThreadActive:
                self.cameraWorker.stop()
                
        self.cameraButton.setText(_translate("MainWindow", "Open Camera"))
    

    def openFileNameDialog(self):
        self.disableCamera()
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
        listPeople = os.listdir("Data")
        personName = self.lineEdit.text()
        self.newFace.name = personName
        print(listPeople)
        print(personName)
        if not personName in listPeople:    
            self.createNewPerson() 
        else:
            self.saveFace()
        self.output.setText(personName + " has been Added!")
        self.lineEdit.setDisabled(True)
        self.lineEdit.setText("")
        self.addNewPerson.setDisabled(True)

    def saveFace(self):
        listFiles = os.listdir("Data/" + self.newFace.name)
        if(len(listFiles) <= 9):
            numpy.save("Data/"+ self.newFace.name+ "/" + self.newFace.name + str(len(listFiles) + 1),self.newFace.encoding)

    
        
    def createNewPerson(self):
        os.mkdir("Data/" + self.newFace.name)
        listFiles = os.listdir("Data/" + self.newFace.name)
        numpy.save("Data/"+ self.newFace.name+ "/" + self.newFace.name + str(len(listFiles) + 1),self.newFace.encoding)

    def startCamera(self):
        _translate = QtCore.QCoreApplication.translate
        if self.cameraWorker.ThreadActive:
            self.cameraWorker.saveImage()
            time.sleep(1)
            self.imageToFind.setPixmap(QPixmap("CameraResult/c1.png"))
            self.detectButton.setDisabled(False)
            self.cameraButton.setText(_translate("MainWindow", "Open Camera"))
            self.filename = "CameraResult/c1.png"
        else:
            self.cameraWorker.start()
            self.cameraWorker.ImageUpdate.connect(self.ImageUpdateSlot)
            self.cameraButton.setText(_translate("MainWindow", "Take Photo"))
            self.detectButton.setDisabled(True)
       
        
        
        
                
        
        
    
    def detectFace(self):
        self.thread = DetectThread()
        self.thread.filename = self.filename
        self.thread.finished.connect(self.detectFinish)
        self.thread.start()
        
        
    def detectFinish(self):
        self.newFace = self.thread.newFace
        _translate = QtCore.QCoreApplication.translate
        if not self.thread.result:
            self.output.setText(_translate("MainWindow","Face not found, Insert another Image"))
        elif self.thread.name != "Unknown":
            self.output.setText(_translate("MainWindow","This is " + self.thread.name))
            self.saveFace()
        elif self.thread.name == "Unknown":
            self.output.setText(_translate("MainWindow","Person Unknown \nClick button below to add new person"))
            self.addNewPerson.setDisabled(False)
            self.lineEdit.setDisabled(False)
        
        self.detectButton.setDisabled(True)

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Recognition"))
        self.uploadButton.setText(_translate("MainWindow", "Choose File"))
        self.cameraButton.setText(_translate("MainWindow", "Open Camera"))
        self.detectButton.setText(_translate("MainWindow", "Detect Face"))
        self.output.setText(_translate("MainWindow", "Person Name"))
        self.addNewPerson.setText(_translate("MainWindow", "Add"))
        
    def ImageUpdateSlot(self, Image):
        self.imageToFind.setPixmap(QPixmap.fromImage(Image))
        
    def CancelFeed(self):
        self.cameraWorker.stop()



class DetectThread(QThread):
    filename = ""
    name = "Unknown"
    result = False

    def run(self):
        self.newFace = Face("",self.filename)
        
        if self.newFace.result:
            self.result = True
            self.name = self.newFace.findPerson()
        else:
            self.result = False
        

class CameraThread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    ThreadActive = False
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while self.ThreadActive:
            ret, self.frame = Capture.read()           
            if ret:
                self.Image = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                self.FlippedImage = cv2.flip(self.Image, 1)
                ConvertToQtFormat = QImage(self.FlippedImage.data, self.FlippedImage.shape[1], self.FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                
    def saveImage(self):
        print("Image saved")
        image = cv2.cvtColor(self.frame, cv2.COLOR_RGBA2RGB)
        flippedImage = cv2.flip(image,1)
        cv2.imwrite('CameraResult/c1.png',flippedImage)
        # cv2.destroyAllWindows()
        self.stop()
                
    def stop(self):
        self.ThreadActive = False



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



