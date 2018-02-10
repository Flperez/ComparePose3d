import sys
import signal
from interfaces.interfaces import Interfaces
from interfaces.threadint import ThreadInt
from matplotlib import pyplot as plt
from time import time
from drawnow import drawnow
from interfaces.interfaces import PosXYZRPY
from plot_data import plot_data


signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':



    interface = Interfaces(sys.argv[1])
    

    t1 = ThreadInt(interface)
    t1.start()



    #Plot data
    run = True



    Pose_real_array = []
    Pose_estimated_array = []
    Error_array = []
    timepoints = []
    start_time = time()
    view_time = 30
    k=1
    while run:

        Pose_real = PosXYZRPY(interface.getsimPose3D())
        Pose_real_array.append(Pose_real)
        Pose_estimated = PosXYZRPY(interface.getPose3D())
        Pose_estimated_array.append(Pose_estimated)
        Error = PosXYZRPY(interface.getError())
        Error_array.append(Error)

        timepoints.append(time() - start_time)






        current_time = timepoints[-1]
        print(current_time)
       # slide the viewing frame along
        if current_time > view_time:
            print("Saving images")
            fig1, fig2,fig3,fig4,fig5 = plot_data(Pose_real=Pose_real_array,
                                         Pose_estimated=Pose_estimated_array,
                                         Error=Error_array,
                                         t=timepoints)
            fig1.savefig("RealvsEstimatedXYZ.png")
            fig2.savefig("RealvsEstimatedRYP.png")

            fig3.savefig("ErrorXYZ.png")
            fig4.savefig("ErrorRYP.png")
            fig5.savefig("ErrorSQRT.png")
            run = False







    


   
