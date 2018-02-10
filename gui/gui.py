from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget,QCheckBox,QPushButton,QLineEdit
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import math
import jderobot
import numpy as np
import sys
import pyqtgraph as pg

class Gui(QWidget):

    def __init__(self, opt):
        super(Gui, self).__init__()
        self.initUI()

    def initUI(self):

        ### Text out
        self.textbox = QLineEdit(self)
        self.textbox.move(20,480+10)
        self.textbox.resize(640,80)



        ### To select a different graph
        self.showNow = None
        
        ## XYZ
        self.cbxyz = QCheckBox('Show XYZ', self)
        self.cbxyz.move(640+40, 100)
        self.cbxyz.toggle()
        self.cbxyz.setChecked(False)
        self.cbxyz.stateChanged.connect(self.showXYZ)

        ## RPY
        self.cbRPY = QCheckBox('Show RPY', self)
        self.cbRPY.move(640+40, 200)
        self.cbRPY.toggle()
        self.cbRPY.setChecked(False)
        self.cbRPY.stateChanged.connect(self.showRPY)

        ## Error
        self.cbError = QCheckBox('Show Error', self)
        self.cbError.move(640+40, 300)
        self.cbError.toggle()
        self.cbError.setChecked(False)
        self.cbError.stateChanged.connect(self.showError)



        ### Saving results
        ButtonSave = QPushButton('Save results', self)
        ButtonSave.setCheckable(True)
        ButtonSave.move(640+50, 480+30)
        ButtonSave.clicked[bool].connect(self.savingResult)

        self.setGeometry(600, 600, 250, 150)
        self.setWindowTitle('Compare')
        self.setFixedSize(10+640+20+150,600)
        self.show()

    def showXYZ(self,state):
        if state == Qt.Checked:
            self.textbox.setText("You have selected show XYZ graph")
            self.showNow = "showXYZ"
            self.cbRPY.setChecked(False)
            self.cbError.setChecked(False)

    def showRPY(self, state):
        if state == Qt.Checked:
            self.textbox.setText("You have selected show RPY graph")
            self.showNow = "showRPY"
            self.cbxyz.setChecked(False)
            self.cbError.setChecked(False)


            

    def showError(self, state):
        if state == Qt.Checked:
            self.textbox.setText("You have selected show error graph")
            self.showNow = "showError"
            self.cbxyz.setChecked(False)
            self.cbRPY.setChecked(False)

            
    def savingResult(self):
        self.textbox.setText("Saving result...")






