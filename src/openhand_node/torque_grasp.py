#!/usr/bin/python3 -i

#Created by gao
#HSH
#Updated 29/01/2024

#main program

#from lib_robotis_mod import *
from hands import Model_O
from syncRW_XMHandler import *
from registerDict import *
from RW_Function import *
import time
import keyboard

def getloads():
    load_values = [] 
    for servo in O.servos: 
        if servo.servo_id in [1, 3, 4]: 
            load_values.append(servo.read_load())
    return load_values

def getpositions():
    position_values = np.array([O.readMotor(i)[0] for i in range(1,len(O.servos))])
    return position_values

######close######
def Close():
    print("close")
    enable_torque([s1,s3,s4],[0,0,0])
    current_mode([s1,s3,s4])
    enable_torque([s1,s3,s4],[1,1,1])
    set_current([s1,s3,s4],[20,-25,20])
    stop = False
    grasped_object = False
    start_time = time.time()
    while not stop:
        Loads = getloads()
        Positions = getpositions()
        print(Positions)
        s1_not_grasp = (Positions[0] > 0.45)
        s3_not_grasp = (Positions[1] > 0.45)
        s4_not_grasp = (Positions[2] > 0.45) 

        if time.time() - start_time > 3 and not(s1_not_grasp and s3_not_grasp and s4_not_grasp) :
            grasped_object = True 
            stop = True
        elif s1_not_grasp or s3_not_grasp or s4_not_grasp:
            print("exceed safe position, reset!")
            print("Did not grasp any object")
            stop = True

    if grasped_object:
        print("Object grasped!")
        print("-----------------")
        print("Press ENTER to release the object")
        keyboard.wait('enter')
        enable_torque([s1,s3,s4],[0,0,0])
        position_mode([s1,s3,s4])
        enable_torque([s1,s3,s4],[1,1,1])
        O.reset()
        enable_torque([s1,s3,s4],[0,0,0])
        print("Object released!")
    else:
        enable_torque([s1,s3,s4],[0,0,0])
        position_mode([s1,s3,s4])
        enable_torque([s1,s3,s4],[1,1,1])
        O.reset()
        enable_torque([s1,s3,s4],[0,0,0])
######pinch_close######
def Pinch_close():
    print("pinch_close")
    enable_torque([s1,s3],[0,0])
    current_mode([s1,s3])
    enable_torque([s1,s3],[1,1])
    set_current([s1,s3],[20,-25])
    stop = False
    grasped_object = False
    start_time = time.time()
    while not stop:
        Loads = getloads()
        Positions = getpositions()
        print(Positions)
        s1_not_grasp = (Positions[0] > 0.45)
        s3_not_grasp = (Positions[1] > 0.45)

        if time.time() - start_time > 3 and not(s1_not_grasp and s3_not_grasp) :
            grasped_object = True 
            stop = True
        elif s1_not_grasp or s3_not_grasp:
            print("exceed safe position, reset!")
            print("Did not grasp any object")
            stop = True

    if grasped_object:
        print("Object grasped!")
        print("-----------------")
        print("Press ENTER to release the object")
        keyboard.wait('enter')
        enable_torque([s1,s3],[0,0])
        position_mode([s1,s3])
        enable_torque([s1,s3],[1,1])
        O.reset()
        enable_torque([s1,s3],[0,0])
        print("Object released!")
    else:
        enable_torque([s1,s3],[0,0])
        position_mode([s1,s3])
        enable_torque([s1,s3],[1,1])
        O.reset()
        enable_torque([s1,s3],[0,0])

######power_close######
def Power_close():
    print("power_close")
    O.adduct()
    enable_torque([s1,s3,s4],[0,0,0])
    current_mode([s1,s3,s4])
    enable_torque([s1,s3,s4],[1,1,1])
    set_current([s1,s3,s4],[20,-25,20])
    stop = False
    grasped_object = False
    start_time = time.time()
    while not stop:
        Loads = getloads()
        Positions = getpositions()
        print(Positions)
        s1_not_grasp = (Positions[0] > 0.6)
        s3_not_grasp = (Positions[1] > 0.6)
        s4_not_grasp = (Positions[2] > 0.6) 

        if time.time() - start_time > 3 and not(s1_not_grasp and s3_not_grasp and s4_not_grasp) :
            grasped_object = True 
            stop = True
        elif s1_not_grasp or s3_not_grasp or s4_not_grasp:
            print("exceed safe position, reset!")
            print("Did not grasp any object")
            stop = True

    if grasped_object:
        print("Object grasped!")
        print("-----------------")
        print("Press ENTER to release the object")
        keyboard.wait('enter')
        enable_torque([s1,s3,s4],[0,0,0])
        position_mode([s1,s3,s4])
        enable_torque([s1,s3,s4],[1,1,1])
        O.reset()
        enable_torque([s1,s3,s4],[0,0,0])
        print("Object released!")
    else:
        enable_torque([s1,s3,s4],[0,0,0])
        position_mode([s1,s3,s4])
        enable_torque([s1,s3,s4],[1,1,1])
        O.reset()
        enable_torque([s1,s3,s4],[0,0,0])

#Initialization
O = Model_O("/dev/ttyUSB0", 2, 1, 3, 4, "XM")
#Close()
#Pinch_close()
Power_close()
