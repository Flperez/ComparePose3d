import sys
import signal
from interfaces.interfaces import Interfaces
from interfaces.threadint import ThreadInt
from matplotlib import pyplot as plt
from time import time
from drawnow import drawnow
from interfaces.interfaces import PosXYZRPY
from plot_data import plot_data
from gui.gui import Gui
from PyQt5.QtWidgets import  QApplication


signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    #interface = Interfaces(sys.argv[1])
    #t1 = ThreadInt(interface)
    #t1.start()
    app = QApplication(sys.argv)
    window = Gui(opt="sim")
    sys.exit(app.exec_())






    


   
