#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################
# Header
import rospy
import time
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
# import PSU_serial as PSU
from scipy.linalg import pinv
from calculate_voltage import *
import sys
import signal

from std_msgs.msg import String, Float32MultiArray
from sensor_msgs.msg import Joy

btn_X = 0
btn_B = 0    # 조이스틱 X, B 버튼 값을 저장할 전역 변수 초기화

## node 비정상 작동 시 강제 종료를 위한 함수 ##
def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


## 조이스틱 값 받아오는 함수 ##
def joycallback(data):
    global btn_X, btn_B

    btn_X = data.buttons[3]   # X 버튼 값 저장
    btn_B = data.buttons[1]   # B 버튼 값 저장




test_mode = 0

# if test_mode == 0:
#     PSU.Turn_on()

t = 0
dt = 0.05
operation_time = 60  # operation time

# while t <= operation_time:
#     start_time = time.time()  # starts time

#     # V1 = V(t)[0, 0]
#     # V2 = V(t)[0, 1]

#     # print(V2)

#     if test_mode == 0:
#         PSU.Transmit_DC(V(t)[0, 0], V(t)[0, 1])
    
#     dt = time.time() - start_time  # calculate time
#     t += dt

#####################################################

# while t <= operation_time:

#     # V1 = V(t)[0, 0]
#     # V2 = V(t)[0, 1]

#     # print(V2)

#     if test_mode == 0:
#         PSU.Transmit_DC(V(t)[0, 0], V(t)[0, 1])

#     time.sleep(dt)
#     t += dt

# if test_mode == 0:
#     PSU.Turn_off()



##############
### 메인함수 ###
##############

def main():
    global t, operation_time, test_mode, btn_B, btn_X

    rospy.init_node('main', anonymous=True)  # node 초기 설정

    #### 메세지 구독 구간 ####
    rospy.Subscriber('/joy', Joy, joycallback)

    #### 메세지 발행 구간 ####
    pub = rospy.Publisher('c_mag_msgs', String, queue_size=10)
    pub_volt = rospy.Publisher('c_mag_volt', Float32MultiArray, queue_size=10)
    pub_actuation = rospy.Publisher('c_mag_actuation', Float32MultiArray, queue_size=10)


    rate = rospy.Rate(100) # 해당 node의 제어주기 설정(실시간성은 보장 안 됨): 100hz 


    while not rospy.is_shutdown():

        psu_on_cmd = True
        psu_off_cmd = True

        v_value = Float32MultiArray()                 # publish 하기 위해 변수를 해당 형식으로 초기화
        actuation_value = Float32MultiArray()
        matrix = actuation    # 전류 센서 node에서 자기장 값을 구하기 위한 인자 전달

        if test_mode == 0:     # test mode 1: helical 알고리즘 구현

            # v_value.data = [V(t)[0, 0], V(t)[0, 1]]       # publish 할 전압 값을 변수에 대입
            v_value.data = [10, 10]    # 테스트

            actuation_value.data = matrix.flatten().tolist()

            pub_volt.publish(v_value)
            pub_actuation.publish(actuation_value)
            pub.publish("Transmit_DC")
            
        
            # # 시간을 의미하는 변수 t가 10을 넘으면 while문 탈출
            # if t >= operation_time:
            #     # PSU.Turn_off()      # PSU 종료
            #     pub.publish("Turn_off")
            #     break               # 반복문 종료

            t += dt   # 시간 값에 대한 증분 구현

        if btn_B == 0 and btn_X == 1:    # X 버튼 누르면 PSU 통신 및 MNS 종료
            if psu_off_cmd == True:
                pub.publish("Turn_off")
                psu_off_cmd = False
                psu_on_cmd = True
            
        
        rate.sleep()

    rospy.spin()




if __name__ == '__main__':
    main()