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
    velocity_mode([s1,s3,s4])
    enable_torque([s1,s3,s4],[1,1,1])
    set_velocity([s1,s3,s4],[3,-4,4])
    stop = False
    grasped_object = False
    s1_vel = False
    s3_vel = False
    s4_vel = False
    is_load = False
    while not stop:
        Loads = getloads()
        Positions = getpositions()
        print(Loads)
        s1_not_grasp = (Positions[0] > 0.4 and abs(Loads[0]) < 40)
        s3_not_grasp = (Positions[1] > 0.4 and abs(Loads[1]) < 40)
        s4_not_grasp = (Positions[2] > 0.4 and abs(Loads[2]) < 40) 

        # Check if any load value is greater than or equal to 50
        for i, (load, position) in enumerate(zip(Loads, Positions), start=1):
            if abs(load) >= 50:
                is_load = True
                # Change the motor to torque_mode
                if i == 1 and not s1_vel:
                    print("Load s1 exceeds 40, set velocity to 0")
                    set_velocity([s1],[0])
                    s1_vel=True
                elif i == 2 and not s3_vel:
                    print("Load s3 exceeds 40, set velocity to 0")
                    set_velocity([s3],[0])
                    s3_vel=True
                elif i == 3 and not s4_vel:
                    print("Load s4 exceeds 40, set velocity to 0")
                    set_velocity([s4],[0])
                    s4_vel=True
                if s1_vel and s3_vel and s4_vel:
                    grasped_object = True 
                    stop = True  

            elif is_load and (s1_not_grasp or s3_not_grasp or s4_not_grasp):
                print("please position the object correctly")
                set_velocity([s1,s3,s4],[0,0,0])
                stop = True

            elif s1_not_grasp and not s1_vel and not is_load:
                set_velocity([s1],[0])
                s1_vel = True
                print("s1 stop")
            elif s3_not_grasp and not s3_vel and not is_load:
                set_velocity([s3],[0])
                s3_vel = True
            elif s4_not_grasp and not s4_vel and not is_load: 
                set_velocity([s4],[0])
                s4_vel = True    
            if s1_not_grasp and s3_not_grasp and s4_not_grasp:
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
        set_velocity([s1,s3,s4],[0,0,0])
        enable_torque([s1,s3,s4],[0,0,0])
        position_mode([s1,s3,s4])
        enable_torque([s1,s3,s4],[1,1,1])
        O.reset()
        enable_torque([s1,s3,s4],[0,0,0])
######pinch_close######
def Pinch_close():
    print("pinch_close")
    enable_torque([s1,s3],[0,0])
    velocity_mode([s1,s3])
    enable_torque([s1,s3],[1,1])
    set_velocity([s1,s3],[3,-4])
    stop = False
    grasped_object = False
    s1_vel = False
    s3_vel = False
    is_load = False
    while not stop:
        Loads = getloads()
        Positions = getpositions()
        print(Loads)
        s1_not_grasp = (Positions[0] > 0.4 and abs(Loads[0]) < 40)
        s3_not_grasp = (Positions[1] > 0.4 and abs(Loads[1]) < 40)

        # Check if any load value is greater than or equal to 50
        for i, (load, position) in enumerate(zip(Loads, Positions), start=1):
            if abs(load) >= 50:
                is_load = True
                # Change the motor to torque_mode
                if i == 1 and not s1_vel:
                    print("Load s1 exceeds 40, set velocity to 0")
                    set_velocity([s1],[0])
                    s1_vel=True
                elif i == 2 and not s3_vel:
                    print("Load s3 exceeds 40, set velocity to 0")
                    set_velocity([s3],[0])
                    s3_vel=True
                if s1_vel and s3_vel:
                    grasped_object = True 
                    stop = True  

            elif is_load and (s1_not_grasp or s3_not_grasp):
                print("Error! please position the object correctly")
                set_velocity([s1,s3],[0,0])
                stop = True

            elif s1_not_grasp and not s1_vel and not is_load:
                set_velocity([s1],[0])
                s1_vel = True
                print("s1 stop")
            elif s3_not_grasp and not s3_vel and not is_load:
                set_velocity([s3],[0])
                s3_vel = True   
            if s1_not_grasp and s3_not_grasp:
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
        set_velocity([s1,s3],[0,0])
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
    velocity_mode([s1,s3,s4])
    enable_torque([s1,s3,s4],[1,1,1])
    set_velocity([s1,s3,s4],[3,-4,4])
    stop = False
    grasped_object = False
    s1_vel = False
    s3_vel = False
    s4_vel = False
    is_load = False
    while not stop:
        Loads = getloads()
        Positions = getpositions()
        s1_not_grasp = (Positions[0] > 0.6 and abs(Loads[0]) < 40)
        s3_not_grasp = (Positions[1] > 0.6 and abs(Loads[1]) < 40)
        s4_not_grasp = (Positions[2] > 0.6 and abs(Loads[2]) < 40) 

        # Check if any load value is greater than or equal to 50
        for i, (load, position) in enumerate(zip(Loads, Positions), start=1):
            if abs(load) >= 50:
                is_load = True
                # Change the motor to torque_mode
                if i == 1 and not s1_vel:
                    print("Load s1 exceeds 40, set velocity to 0")
                    set_velocity([s1],[0])
                    s1_vel=True
                elif i == 2 and not s3_vel:
                    print("Load s3 exceeds 40, set velocity to 0")
                    set_velocity([s3],[0])
                    s3_vel=True
                elif i == 3 and not s4_vel:
                    print("Load s4 exceeds 40, set velocity to 0")
                    set_velocity([s4],[0])
                    s4_vel=True
                if s1_vel and s3_vel and s4_vel:
                    grasped_object = True 
                    stop = True  

            elif is_load and (s1_not_grasp or s3_not_grasp or s4_not_grasp):
                print("Error! please position the object correctly")
                set_velocity([s1,s3,s4],[0,0,0])
                stop = True

            elif s1_not_grasp and not s1_vel and not is_load:
                set_velocity([s1],[0])
                s1_vel = True
            elif s3_not_grasp and not s3_vel and not is_load:
                set_velocity([s3],[0])
                s3_vel = True
            elif s4_not_grasp and not s4_vel and not is_load: 
                set_velocity([s4],[0])
                s4_vel = True    
            if s1_not_grasp and s3_not_grasp and s4_not_grasp:
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
        set_velocity([s1,s3,s4],[0,0,0])
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
