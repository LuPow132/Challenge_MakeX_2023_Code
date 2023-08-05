#Import Library
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild import power_manage_module
from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild.smartservo import smartservo_class
from mbuild.ranging_sensor import ranging_sensor_class
import math
import time
import novapi

#-----Configuration-----#




#-----Assign Module Port-----#

#Encode Motor#
encode_FL = encoder_motor_class("M1", "INDEX1")
encode_FR = encoder_motor_class("M2", "INDEX1")
encode_Rear = encoder_motor_class("M3", "INDEX1")

#Arm motor
servo_arm_L = smartservo_class("M6", "INDEX1")
servo_arm_R = smartservo_class("M6", "INDEX2")

#Camera Pin
smart_cam = smart_camera_class("PORT3", "INDEX1")
smart_cam.set_mode("color")

#Ranging sensor port
ball_checker = ranging_sensor_class("PORT2", "INDEX1")


#-----System Variable-----#

#Some function that novapi too lazy to put it in#

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

#Class that management the motor job things
class motor:
    def drive(spd1,spd2,spd3):
        encode_FL.set_power(spd1)
        encode_FR.set_power(spd2)
        encode_Rear.set_power(spd3)

    
    
