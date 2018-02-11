import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QTimer
import numpy as np
from operator import attrgetter


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, option,parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.axes = fig.add_subplot(111)
        self.setParent(parent)
        print option
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, option,map,posesim,posereal,error,parent=None, width=5, height=4, dpi=100):
        MyMplCanvas.__init__(self, option,parent, width, height, dpi)
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(100)
        self.option = option
        self.posesim = posesim
        self.posereal = posereal
        self.error = error
        self.map = map
    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        if self.option == "showXYZ":
            xEstimated = list(map(attrgetter('x'), self.posesim))
            yEstimated = list(map(attrgetter('y'), self.posesim))

            xReal = list(map(attrgetter('x'), self.posereal))
            yReal = list(map(attrgetter('y'), self.posereal))

            xmap = list(map(attrgetter('x'), self.map))
            ymap = list(map(attrgetter('y'), self.map))
            self.axes.plot(xEstimated,yEstimated, 'r',xReal,yReal,'b',xmap,ymap,'*k')
            self.draw()



    def setOption(self,option):
        self.option=option

class MyplotXYZ(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, xmap,ymap,xsim,ysim,xreal,yreal,parent=None, width=5, height=4, dpi=100):
        MyMplCanvas.__init__(self,parent=parent, width=width, height=height, dpi=dpi,option="showXYZ")
        self.xmap = xmap
        self.ymap = ymap
        self.xsim = xsim
        self.ysim = ysim
        self.xreal = xreal
        self.yreal = yreal
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(250)

    def update(self):
        self.axes.plot(self.xmap, self.ymap, '*k', self.xsim, self.ysim, 'r', self.xreal, self.yreal, 'b')
        self.draw()


class MyplotRPY(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, Rreal, Yreal, Preal, Rsim, Ysim, Psim, parent=None, width=5, height=4, dpi=100):
        MyMplCanvas.__init__(self, parent=parent, width=width, height=height, dpi=dpi, option="showRPY")
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(250)
        self.Rreal = Rreal
        self.Yreal = Yreal
        self.Preal = Preal
        self.Rsim = Rsim
        self.Ysim = Ysim
        self.Psim = Psim

    def update(self):
        t = np.linspace(0,len(self.Rreal),len(self.Rreal))
        self.axes[0].plot(t,self.Rreal,t,self.Rsim)
        self.axes[1].plot(t, self.Yreal, t, self.Ysim)
        self.axes[2].plot(t, self.Preal, t, self.Psim)
        self.draw()
