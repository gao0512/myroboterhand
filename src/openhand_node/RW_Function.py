#!/usr/bin/python -i

#Created by gao
#HSH
#Updated 26/01/2024

#sync read, write-functions


from hands import Model_O
from syncRW_XMHandler import *
from registerDict import *

def velocity_mode(servos):
    if servos == [s1,s3,s4]:
        val = [1,1,1]
    elif servos == [s1,s3]:
        val = [1,1]    
    address_str = "ADDR_OPERATING_MODE" 
    sync_write(servos, address_str, val, 1)

def position_mode(servos):
    if servos == [s1,s3,s4]:
        val = [3,3,3]
    elif servos == [s1,s3]:
        val = [3,3]    
    address_str = "ADDR_OPERATING_MODE" 
    sync_write(servos, address_str, val, 1)

def current_mode(servos):
    if servos == [s1,s3,s4]:
        val = [0,0,0]
    elif servos == [s1,s3]:
        val = [0,0]    
    address_str = "ADDR_OPERATING_MODE" 
    sync_write(servos, address_str, val, 1)

def enable_torque(servos,val):
    address_str = "ADDR_TORQUE_ENABLE" 
    sync_write(servos, address_str, val, 1)

def set_current(servos,val):#val>=15
    address_str = "ADDR_GOAL_CURRENT" 
    sync_write(servos, address_str, val, 2)

def set_velocity(servos,val):
    address_str = "ADDR_GOAL_VELOCITY" 
    sync_write(servos, address_str, val, 4)


