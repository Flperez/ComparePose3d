import sys
import signal
from interfaces.interfaces import Interfaces
from interfaces.threadint import ThreadInt
from matplotlib import pyplot as plt
from time import time
from drawnow import drawnow
from interfaces.interfaces import PosXYZRPY
from gui.gui import Gui
from gui.threadgui import ThreadGui
from PyQt5.QtWidgets import  QApplication

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    interface = Interfaces(sys.argv[1])

    app = QApplication(sys.argv)
    window = Gui(map="markers.txt")
    window.setInterface(interface)

    window.show()

    t1 = ThreadInt(interface)
    t1.start()

    t2 = ThreadGui(window)
    t2.start()


    sys.exit(app.exec_())




    


   
