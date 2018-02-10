from matplotlib import pyplot as plt
from interfaces.interfaces import PosXYZRPY
from numpy import linalg as LA
from operator import attrgetter
from math import sqrt
def plot_data(Pose_real,Pose_estimated,Error,t):

    PosRealx = list(map(attrgetter('x'), Pose_real))
    PosRealy = list(map(attrgetter('y'), Pose_real))
    PosRealz = list(map(attrgetter('z'), Pose_real))

    PosRealR = list(map(attrgetter('R'), Pose_real))
    PosRealY = list(map(attrgetter('Y'), Pose_real))
    PosRealP = list(map(attrgetter('P'), Pose_real))

    PosEstx = list(map(attrgetter('x'), Pose_estimated))
    PosEsty = list(map(attrgetter('y'), Pose_estimated))
    PosEstz = list(map(attrgetter('z'), Pose_estimated))

    PosEstR = list(map(attrgetter('R'), Pose_estimated))
    PosEstY = list(map(attrgetter('Y'), Pose_estimated))
    PosEstP = list(map(attrgetter('P'), Pose_estimated))

    Errorx = list(map(attrgetter('x'), Error))
    Errory = list(map(attrgetter('y'), Error))
    Errorz = list(map(attrgetter('z'), Error))

    ErrorR = list(map(attrgetter('R'), Error))
    ErrorY = list(map(attrgetter('Y'), Error))
    ErrorP = list(map(attrgetter('P'), Error))


    ErrornormXYZ=[sqrt(Errorx[i]**2+Errory[i]**2+Errorz[i]**2) for i in range(0,len(Errorx))]
    ErrornormRYP=[sqrt(ErrorR[i]**2+ErrorY[i]**2+ErrorP[i]**2) for i in range(0,len(Errorx))]

    ######### Figure 1 #####################
    fig1, axarr = plt.subplots(3, sharex=True)

    #### XYZ real y estimado
    axarr[0].plot(t,PosRealx,label="PosReal"),axarr[0].plot(t,PosEstx,label="PosEst"),axarr[0].set_title("x")
    axarr[0].legend(loc='upper center')
    axarr[1].plot(t,PosRealy,label="PosReal"),axarr[1].plot(t,PosEsty,label="PosEst"),axarr[1].set_title("y")
    axarr[1].legend(loc='upper center')
    axarr[2].plot(t,PosRealz,label="PosReal"),axarr[2].plot(t,PosEstz,label="PosEst"),axarr[2].set_title("z")
    axarr[2].legend(loc='upper center')


    ######### Figure 2 #####################
    fig2, axarr = plt.subplots(3, sharex=True)

    ### Angulo RPY
    axarr[0].plot(t,PosRealR,label="PosReal"),axarr[0].plot(t,PosEstR,label="PosEst"),axarr[0].set_title("Roll")
    axarr[0].legend(loc='upper center')
    axarr[1].plot(t,PosRealY,label="PosReal"),axarr[1].plot(t,PosEstY,label="PosEst"),axarr[1].set_title("Yaw")
    axarr[1].legend(loc='upper center')
    axarr[2].plot(t,PosRealP,label="PosReal"),axarr[2].plot(t,PosEstP,label="PosEst"),axarr[2].set_title("Pitch")
    axarr[2].legend(loc='upper center')

    ######### Figure 3 #####################
    fig3, axarr = plt.subplots(3, sharex=True)

    #### XYZ real y estimado
    axarr[0].plot(t, Errorx),axarr[0].set_title("Error x")
    axarr[1].plot(t, Errory),axarr[1].set_title("Error y")
    axarr[2].plot(t, Errorz),axarr[2].set_title("Error z")

    ######### Figure 4 #####################
    fig4, axarr = plt.subplots(3, sharex=True)

    ### Angulo RPY
    axarr[0].plot(t, ErrorR),axarr[0].set_title("Error Roll")
    axarr[1].plot(t, ErrorP),axarr[1].set_title("Error Pitch")
    axarr[2].plot(t, ErrorY),axarr[2].set_title("Error yaw")

    ######### Figure 5 #####################
    fig5, axarr = plt.subplots(2, sharex=True)

    ### Angulo RPY
    axarr[0].plot(t, ErrornormXYZ),axarr[0].set_title("Error cuadratico XYZ")
    axarr[1].plot(t, ErrornormRYP),axarr[1].set_title("Error cuadratico RPY")

    return fig1,fig2,fig3,fig4,fig5