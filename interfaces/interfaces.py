#!/usr/bin/env python3
import sys, traceback, Ice
import easyiceconfig as EasyIce
import jderobot
import numpy as np
import threading
import math


class PosXYZRPY:
    def __init__(self, pose):
        self.x = pose.x
        self.y = pose.y
        self.z = pose.z

        self.R = math.atan2(2 * (pose.q0 * pose.q1 + pose.q2 * pose.q3), 1 - 2 * (pose.q1 ** 2 + pose.q2 ** 2))
        self.P = math.asin(2 * (pose.q0 * pose.q2 - pose.q3 * pose.q1))
        self.Y = math.atan2(2.0 * (pose.q0 * pose.q3 + pose.q1 * 2), 1 - 2 * (pose.q2 * pose.q2 + pose.q3 * pose.q3))


class Interfaces():

    ARDRONE1=0
    ARDRONE2=1
    ARDRONE_SIMULATED=10
    #flat
   
    def __init__(self, opt):
        self.lock = threading.Lock()
        self.lock2 = threading.Lock()
        self.opt = opt
        try:
            ic = EasyIce.initialize(sys.argv)
            properties = ic.getProperties()

            #Connection to ICE interfaces

            #------- POSE3D AUTOLOC ---------


            basepose3D = ic.propertyToProxy("CamAutoloc.Pose3D.Proxy")
            print("Autoloc:",basepose3D)

            self.pose3DProxy=jderobot.Pose3DPrx.checkedCast(basepose3D)
            if self.pose3DProxy:
                self.pose=jderobot.Pose3DData()
            else:
                print ('Interface pose3D not connected')





            #------- POSE3D SIM ---------
            simpose3D = ic.propertyToProxy("CamAutoloc.Pose3Dsim.Proxy")
            print("Simpose: ",simpose3D)
            self.simpose3DProxy=jderobot.Pose3DPrx.checkedCast(simpose3D)
            if self.simpose3DProxy:
                self.simpose=jderobot.Pose3DData()
            else:
                print ('Interface pose3D not connected')







        except:
            traceback.print_exc()
            exit()
            status = 1

        self.pause = True
        self.patherror = 0.0
        #self.takeoff()

    def update(self):
        self.lock.acquire()
        self.updatePose()
        self.lock.release()



    def updatePose(self):
        #if self.pose3DProxy:
        self.pose=self.pose3DProxy.getPose3DData()
        self.simpose=self.simpose3DProxy.getPose3DData()

    def getPose3D(self):
        if self.pose3DProxy:
            self.lock.acquire()
            tmp=self.pose
            self.lock.release()
            return tmp
        else:
            return None

    def getsimPose3D(self):
        if self.simpose3DProxy:
            self.lock.acquire()
            tmp=self.simpose
            self.lock.release()
            return tmp
        else:
            return None



    def getError(self):
        if self.simpose3DProxy and self.pose3DProxy:
            self.lock.acquire()
            error = jderobot.Pose3DData()
            error.x = self.simpose.x - self.pose.x
            error.y = self.simpose.y - self.pose.y
            error.z = self.simpose.z - self.pose.z

            error.q0 = self.simpose.q0 - self.pose.q0
            error.q1 = self.simpose.q1 - self.pose.q1
            error.q2 = self.simpose.q2 - self.pose.q2
            error.q3 = self.simpose.q3 - self.pose.q3
            self.lock.release()

            return error

        else:
            return None

