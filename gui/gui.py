from PyQt5.QtWidgets import QWidget,QCheckBox,QPushButton,QLineEdit,QSizePolicy,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer
import pyqtgraph as pg
import math
import jderobot
from jderobotTypes import pose3d
import numpy as np
import sys,os
from widgetplot import MyplotXYZ,MyplotRPY
from interfaces.interfaces import PosXYZRPY





class Gui(QWidget):

    def __init__(self,map):
        super(Gui, self).__init__()
        self.initUI(map=map)

    def initUI(self,map):
        ### initialize
        self.filename = map
        # Estimated
        self.xestimated = []
        self.yestimated = []
        self.zestimated = []
        self.Restimated = []
        self.Yestimated = []
        self.Pestimated = []

        self.xreal = []
        self.yreal = []
        self.zreal = []
        self.Rreal = []
        self.Yreal = []
        self.Preal = []



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
        self.pathx,self.pathy,self.pathz = Gui.loadpathXYZ(self)

        self.main_widget = QWidget(self)
        l = QVBoxLayout(self.main_widget)

        self.myplot = MyplotXYZ(parent=self.main_widget, width=5, height=4, dpi=100,
                                xmap=self.pathx, ymap=self.pathy,
                                xsim=self.xestimated, ysim=self.yestimated,
                                xreal=self.xreal, yreal=self.yreal)
        l.addWidget(self.myplot)

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
        ## Save real and sim xyzRYP
        np.save(os.path.join("result","xestimated.npy"),np.array(self.xestimated))
        np.save(os.path.join("result","yestimated.npy"),np.array(self.yestimated))
        np.save(os.path.join("result","xreal.npy"),np.array(self.xreal))
        np.save(os.path.join("result","yreal.npy"),np.array(self.yreal))
        self.textbox.setText("Done!")





    def setInterface(self,interface):
        self.interface=interface

    def update(self):

        ###### Estimated ########
        pose3dEstimated = PosXYZRPY(self.interface.getsimPose3D())
        self.xestimated.append(pose3dEstimated.x)
        self.yestimated.append(pose3dEstimated.y)
        self.zestimated.append(pose3dEstimated.z)
        self.Restimated.append(pose3dEstimated.R)
        self.Yestimated.append(pose3dEstimated.Y)
        self.Pestimated.append(pose3dEstimated.P)

        ###### Real ########
        pose3dReal = PosXYZRPY(self.interface.getPose3D())
        self.xreal.append(pose3dReal.x)
        self.yreal.append(pose3dReal.y)
        self.zreal.append(pose3dReal.z)
        self.Rreal.append(pose3dReal.R)
        self.Yreal.append(pose3dReal.Y)
        self.Preal.append(pose3dReal.P)

        ##### Error ########
        self.error = PosXYZRPY(self.interface.getError())











    def loadpathXYZ(self):
        xlist = []
        ylist = []
        zlist = []

        for line in open(self.filename, 'r').readlines():
            line = line.rstrip('\n')
            linelist = line.split()
            if len(linelist)>1:

                x = float(linelist[0])
                y = float(linelist[1])
                z = float(linelist[2])

                xlist.append(x)
                ylist.append(y)
                zlist.append(z)
        return xlist,ylist,zlist







