#!/usr/bin/env python
# -*- coding: utf-8 -*-


####################################################################
# THIS SCRIPT WAS WRITTEN FOR SERIAL COMMUNICATION BETWEEN PC AND
# POWER SUPPLY (CSW5550) IN ROS, IT IS TRANSLATING MATLAB PAKAGE
# "Turn_on.m", "Turn_off.m", AND "Transmit_DC.m" INTO PYTHON.
#
#  * Each constant for 'port' and 'baudrate' can be obtained by
#    running '$ dmesg | grep tty' in Linux terminal and by 
#    referring to the device's features, respectively.
#   
#  * Other serial parameters are omitted as they are set to default
#    values, but can be explicitly specified and modified if needed.
#    For more information about pySerial API, check the website:
#    https://pyserial.readthedocs.io/en/latest/pyserial_api.html
#
#  * The data sent to the power supply is written in SCPI (Standard
#    Commands for Programmable Instruments) language. In case to
#    modify, please refer to the device's SCPI programming manual.
#    Even when updated, the newline command "\n" must always be
#    included in the data string. (e.g., "SYSTem:REMote\n")

# import rospy # Import Python client library for ROS
# import serial # Import pySerial library
# from std_msgs.msg import String, Float32MultiArray

# # Serial port opened, serial parameters
# ser = serial.Serial(
#         port="/dev/ttyMP1",
#         baudrate=115200,
#         )
# rate = rospy.Rate(10)  # 10 Hz


# # Activate power supply
# def Turn_on():

#     # Set remote control
#     ser.write("SYSTem:REMote\n".encode('ascii'))
#     # Enable output source
#     ser.write("OUTP 1\n".encode('ascii'))
#     # Set DC mode
#     ser.write("MODE DC\n".encode('ascii'))
#     # Uncouple all output phases
#     ser.write("INSTrument:COUPle NONE\n".encode('ascii'))     

# # Diactivate power supply
# def Turn_off():

#     # Couple all output phases
#     ser.write("INSTrument:COUPle ALL\n".encode('ascii')) 
#     # Set output voltages as zeros
#     ser.write("VOLTage 0\n".encode('ascii'))
#     # Disable output source
#     ser.write("OUTP 0\n".encode('ascii'))
#     # Set local control
#     ser.write("SYSTem:LOCal\n".encode('ascii'))

#     # Serial port closed
#     ser.close()

# # Voltage trasmission to power supply
# def Transmit_DC(V1, V2):

#     # Select output phase 1
#     ser.write("INSTrument:NSELect 1\n".encode('ascii'))
#     # Set voltage for phase 1 
#     ser.write("VOLTage {}\n".format(V1).encode('ascii'))
        
#     # Select output phase 2
#     ser.write("INSTrument:NSELect 2\n".encode('ascii'))
#     # Set voltage for phase 2
#     ser.write("VOLTage {}\n".format(V2).encode('ascii'))


# if __name__ == '__main__':
#     Turn_off()



import rospy # Import Python client library for ROS
import serial # Import pySerial library
from std_msgs.msg import String, Float32MultiArray
import time

## 구독한 메세지를 저장할 전역변수 선언 및 초기화
psu_status = ""   # c_mag_msgs 저장 변수
V_val = [0,0]     # c_mag_volt 저장 변수

# # 각 상에 대한 전류 측정
# phases = [1, 2, 3]  # 3상
# current_readings = {}


# def read_serial_data(ser):
#     try:
#         if ser.in_waiting > 0:  # 버퍼에 읽을 데이터가 있는지 확인
#             data = ser.readline().decode('ascii').strip()  # 데이터 읽기 및 디코딩
#             rospy.loginfo("Received from serial: %s", data)
#             return data
#     except serial.SerialException as e:
#         rospy.logerr("Error reading from serial port: %s", e)
#     return None



def c_mag_callback(data):
    global psu_status
    psu_status = data.data

def volt_callback(data):
    global V_val
    V_val[0] = round(data.data[0], 3)
    V_val[1] = round(data.data[1], 3)

###############
#### 메인문 ####
##############
def PSU_serial():
    global psu_status, V_val, phases, current_readings

    # node 설정
    rospy.init_node('PSU_serial', anonymous=True)

    #### 메세지 구독 구간 ####
    rospy.Subscriber('/c_mag_msgs', String, c_mag_callback)
    rospy.Subscriber('/c_mag_volt', Float32MultiArray, volt_callback)

    #### 메세지 발행 구간 ####


    # Serial port opened, serial parameters
    ser = serial.Serial(port="/dev/ttyMP1",
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)
    rate = rospy.Rate(100)  # 100 Hz


    mode = 0

    # 통신 반복문 설정
    while not rospy.is_shutdown():

        ## 통신 mode 설정 ##
        # if psu_status == "Turn_on": mode = 1
        if psu_status == "Transmit_DC": mode = 2
        elif psu_status == "Turn_off": mode = 3

        # print(psu_status)
        # print(V_val)

        ## 통신 시작 설정
        if mode == 0:
            
            # Set remote control
            ser.write("SYSTem:REMote\n".encode('ascii'))
            # Enable output source
            ser.write("OUTP 1\n".encode('ascii'))
            # Set DC mode
            ser.write("MODE DC\n".encode('ascii'))
            # Uncouple all output phases
            ser.write("INSTrument:COUPle NONE\n".encode('ascii'))

            # mode = 2

        ## helical motion 설정
        elif mode == 2:
            
            # Select output phase 1
            ser.write("INSTrument:NSELect 1\n".encode('ascii'))
            # Set voltage for phase 1 
            ser.write("VOLTage {}\n".format(V_val[0]).encode('ascii'))
            # print("VOLTage {}\n".format(V_val[0]).encode('ascii'))
                
            # Select output phase 2
            ser.write("INSTrument:NSELect 2\n".encode('ascii'))
            # Set voltage for phase 2
            ser.write("VOLTage {}\n".format(V_val[1]).encode('ascii'))


        ## 통신 종료 설정
        elif mode == 3:
            
            # Couple all output phases
            ser.write("INSTrument:COUPle ALL\n".encode('ascii')) 
            # Set output voltages as zeros
            ser.write("VOLTage 0\n".encode('ascii'))
            # Disable output source
            ser.write("OUTP 0\n".encode('ascii'))
            # Set local control
            ser.write("SYSTem:LOCal\n".encode('ascii'))

            # Serial port closed
            ser.close()

        
        # ser.write("MEASure1:CURRent[:DC]?\n".encode('ascii'))
        # received_data = read_serial_data(ser)
        # if received_data:
        #     # 받은 데이터에 대한 처리 로직
        #     rospy.loginfo("Process received data here")


        # for phase in phases:
        #     # 각 상 선택
        #     ser.write('INSTrument:NSELect {}\n'.format(phase).encode('ascii'))
            
        #     # 전류 측정
        #     ser.write('MEASure:CURRent:DC?\n'.encode('ascii'))
            
        #     # 데이터 읽기
        #     response = ser.readline().decode().strip()
        #     current_readings['Phase {}'.format(phase)] = response

        # # 결과 출력
        # for phase, current in current_readings.items():
        #     print("{} Current: {} A".format(phase, current))



        rate.sleep()





if __name__ == '__main__':
    try:
        PSU_serial()
    except rospy.ROSInterruptException:
        pass