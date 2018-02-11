from PyQt5.QtWidgets import QWidget,QCheckBox,QPushButton,QLineEdit,QSizePolicy,QVBoxLayout
from PyQt5.QtCore import Qt,pyqtSignal
import pyqtgraph as pg
import math
import jderobot
from jderobotTypes import pose3d
import numpy as np
import sys,os
from widgetplot import MyplotXYZ,MyplotRPY,MyDynamicMplCanvas
from interfaces.interfaces import PosXYZRPY
from OpenGL.GL import *
from OpenGL.GLU import *




class Gui(QWidget):
    def __init__(self,map,interface):
        super(Gui, self).__init__()
        self.initUI(map=map)
        self.interface = interface

    def initUI(self,map):
        ### initialize
        self.filename = map

        # Estimated
        self.pose3dEstimated = []
        self.pose3dReal = []
        self.error = []

        self.loadpathXYZ()


        ### Text out
        self.textbox = QLineEdit(self)
        self.textbox.move(20,480+10)
        self.textbox.resize(640,80)



        ### To select a different graph
        self.showNow = "showXYZ"
        
        ## XYZ
        self.cbxyz = QCheckBox('Show XYZ', self)
        self.cbxyz.move(640+40, 100)
        self.cbxyz.toggle()
        self.cbxyz.setChecked(True)
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


        # Plot map
        self.main_widget = QWidget(self)
        l = QVBoxLayout(self.main_widget)
        self.dc = MyDynamicMplCanvas(parent=self.main_widget,option=self.showNow,
                                     posesim=self.pose3dEstimated,posereal=self.pose3dReal,error=self.error,
                                     map=self.map)
        l.addWidget(self.dc)




        self.setGeometry(600, 600, 250, 150)
        self.setWindowTitle('Compare')
        self.setFixedSize(10+640+20+150,600)

    def showXYZ(self,state):
        if state == Qt.Checked:
            self.textbox.setText("You have selected show XYZ graph")
            self.showNow = "showXYZ"
            self.dc.setOption(self.showNow)

            self.cbRPY.setChecked(False)
            self.cbError.setChecked(False)

    def showRPY(self, state):
        if state == Qt.Checked:
            self.textbox.setText("You have selected show RPY graph")
            self.showNow = "showRPY"
            self.cbxyz.setChecked(False)
            self.cbError.setChecked(False)
            self.dc.setOption(self.showNow)



            

    def showError(self, state):
        if state == Qt.Checked:
            self.textbox.setText("You have selected show error graph")
            self.showNow = "showError"
            self.dc.setOption(self.showNow)
            self.cbxyz.setChecked(False)
            self.cbRPY.setChecked(False)

            
    def savingResult(self):
        self.textbox.setText("Saving result...")
        ## Save real and sim xyzRYP

        self.textbox.setText("Done!")





    def update_data(self):

        ###### Estimated ########
        self.pose3dEstimated.append(PosXYZRPY(self.interface.getsimPose3D()))

        ###### Real ########
        self.pose3dReal.append(PosXYZRPY(self.interface.getPose3D()))

        ##### Error ########
        self.error.append(PosXYZRPY(self.interface.getError()))





    def loadpathXYZ(self):
        a=[]

        for line in open(self.filename, 'r').readlines():
            line = line.rstrip('\n')
            linelist = line.split()
            if len(linelist)>1:
                pose = jderobot.Pose3DData()
                pose.x = float(linelist[0])
                pose.y = float(linelist[1])
                pose.z = float(linelist[2])
                a.append(pose)

        self.map = list(a)







