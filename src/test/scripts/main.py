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


## node 비정상 작동 시 강제 종료를 위한 함수 ##
def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



test_mode = 0

# if test_mode == 0:
#     PSU.Turn_on()

t = 0
dt = 0.05
operation_time = 30  # operation time

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
    global t, operation_time, test_mode

    rospy.init_node('main', anonymous=True)  # node 초기 설정

    #### 메세지 구독 구간 ####


    #### 메세지 발행 구간 ####
    pub = rospy.Publisher('c_mag_msgs', String, queue_size=10)
    pub_volt = rospy.Publisher('c_mag_volt', Float32MultiArray, queue_size=10)


    rate = rospy.Rate(100) # 해당 node의 제어주기 설정(실시간성은 보장 안 됨): 100hz 


    while not rospy.is_shutdown():

        # if test_mode <= 0.9:     # test mode 0: 실험 시작 준비 
        #     pub.publish("Turn_on")  # PSU 전원 ON
        #     test_mode = 1           # 다음 단계로 진행

        if test_mode == 0:     # test mode 1: helical 알고리즘 구현
            v_value = Float32MultiArray()                 # publish 하기 위해 변수를 해당 형식으로 초기화
            # v_value.data = [V(t)[0, 0], V(t)[0, 1]]       # publish 할 값을 변수에 대입
            v_value.data = [30, 30]
            pub_volt.publish(v_value)
            pub.publish("Transmit_DC")
        
            # 시간을 의미하는 변수 t가 10을 넘으면 while문 탈출
            if t >= operation_time:
                # PSU.Turn_off()      # PSU 종료
                pub.publish("Turn_off")
                break               # 반복문 종료

            t += dt   # 시간 값에 대한 증분 구현

        rate.sleep()

    rospy.spin()




if __name__ == '__main__':
    main()