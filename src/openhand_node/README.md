--------------
lib_robotis_mod.py
--------------
sudo python3 lib_robotis_mod.py -d '/dev/ttyUSB0' --scan
sudo python3 lib_robotis_mod.py -d '/dev/ttyUSB0' --setID 1 5


--------------
hands.py
--------------
sudo python3 -i hands.py
(or: python -i hands.py)
O = Model_O("/dev/ttyUSB0",2,1,3,4,"XM")
O.close()
O.reset()


--------------
syncRW_XMHandler.py
--------------
sudo python3 syncRW_XMHandler.py


--------------
torque_grasp.py
--------------
sudo python3 torque_grasp.py


--------------
velocity_grasp.py
--------------
sudo python3 velocity_grasp.py
