from lib_robotis_mod import *
from registerDict import *
from hands import *
import struct


def sync_write(servos, address, values, reg_size=4):

    addresses = [registerDict.X_Series[address]] * len(servos) # Zieladresse
    header = [0xFF, 0xFF, 0xFD, 0x00] + [0xFE]
    INST = 0x83 # Sync Write
    P1, P2 = DXL_LOBYTE(addresses[0]), DXL_HIBYTE(addresses[0])
    P3, P4 = reg_size, 0x00 # Parameter

    total_packet_length = registerDict.DXL_MAKEWORD(P3, P4) * len(servos) + len(servos) + 7

    LEN1, LEN2 = DXL_LOBYTE(total_packet_length), DXL_HIBYTE(total_packet_length)

    msg = []
    print(f"Writing to {address} with values: {values}")
    for servo_idx, servo in enumerate(servos):
        msg = msg + [servo.servo_id] # Servos-ID
        value = values[servo_idx]
        for i in range(reg_size):
            msg += [(value >> (8 * i)) & 0xFF]

    msg = header + [LEN1, LEN2, INST, P1, P2, P3, P4] + msg
    crc = registerDict.updateCRC(0, msg, total_packet_length + 5)
    # Pruefziffer
    msg = msg + [DXL_LOBYTE(crc), DXL_HIBYTE(crc)]
    # Das zu schickende Paket
    return send_msg(servos, msg, reg_size)

def sync_read(servos, address, reg_size=4):
    addresses = [registerDict.X_Series[address]] * len(servos)
    header = [0xFF, 0xFF, 0xFD, 0x00] + [0xFE]

    msg_len = 5 + len(servos) * 1 + 2
    # header + servo_ids + CRC
    LEN1, LEN2 = DXL_LOBYTE(msg_len), DXL_HIBYTE(msg_len)
    INST = 0x82 # Sync Read
    P1, P2 = DXL_LOBYTE(addresses[0]), DXL_HIBYTE(addresses[0])
    P3, P4 = reg_size, 0x00

    msg = [servo.servo_id for servo in servos]
    msg = header + [LEN1, LEN2, INST, P1, P2, P3, P4] + msg
    crc = registerDict.updateCRC(0, msg, len(msg))
    msg = msg + [DXL_LOBYTE(crc), DXL_HIBYTE(crc)]

    return send_msg(servos, msg, reg_size)

def send_msg(servos, msg, reg_size=0):
    
    dyn.acq_mutex()
    try:
        out = b''
        for m in msg:
            out += chr(m).encode('latin1')
        dyn.send_serial(out)
        data = receive_reply(servos, reg_size)
    except Exception as inst:
        dyn.rel_mutex()
        raise RuntimeError(repr(str(inst)))
    dyn.rel_mutex() # Mutex freigeben

    return data

def receive_reply(servos, reg_size):
    data = []
    for servo in servos:
        single_read = dyn.read_serial(11 + reg_size)
        if len(single_read) == 0: # keine Rueckmeldung
            return None
        if single_read[4]!= servo.servo_id:
            # Fehler austritt
            raise RuntimeError('lib_robotis: Incorrect servo ID received')
        else:
            if reg_size == 1:
                value = single_read[9]
            else:
                value_bytes = single_read[9: 9 + reg_size]
                value = int.from_bytes(value_bytes, byteorder='little', signed=False)
            data.append(value)

    return data

#dyn = USB2Dynamixel_Device()
#s1 = Robotis_Servo_X(dyn, 2, 'XM')
#s2 = Robotis_Servo_X(dyn, 1, 'XM')
#s3 = Robotis_Servo_X(dyn, 3, 'XM')
#s4 = Robotis_Servo_X(dyn, 4, 'XM')
#servos = [s1, s2, s3, s4]

#address_str = "ADDR_PRESENT_POSITION" 
#read = sync_read(servos, address_str, 4)
#print(read)

#values=[0,0,0,0]
#sync_write(servos, address_str, values, 1)
dyn = USB2Dynamixel_Device()
s1 = Robotis_Servo_X(dyn, 1, 'XM')
s2 = Robotis_Servo_X(dyn, 2, 'XM')
s3 = Robotis_Servo_X(dyn, 3, 'XM')
s4 = Robotis_Servo_X(dyn, 4, 'XM')
servos = [s1, s2, s3, s4]




