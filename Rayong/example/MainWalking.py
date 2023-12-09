#import library
from mbuild import power_expand_board
from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild.smartservo import smartservo_class
from mbuild import gamepad
from mbuild import power_manage_module
from mbuild.ranging_sensor import ranging_sensor_class
import math
import time
import novapi

#-----Configuration-----#

#Assign each encode ,servo motor ,camera

#drive encode motor
encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

#Sensitivity
sensitivity_rot = 0.7

#---Class and Function---#

class motors:

    #drive each motors in one function
    def drive(v1:int, v2:int, v3:int, v4:int):
        encode_fl.set_power(v1 * -1)
        encode_fr.set_power(v2)
        encode_rl.set_power(v3 * -1)
        encode_rr.set_power(v4)

    def holonomic(speed:int,strafe:int,rot:int):

        leftFront = speed + rot + strafe
        rightFront = speed - rot - strafe
        leftBack = speed + rot - strafe
        rightBack = speed - rot + strafe

        motors.drive(leftFront,rightFront,leftBack,rightBack)


class program:

    #manual program
    def manual():
        x = gamepad.get_joystick("Lx")
        y = gamepad.get_joystick("Ly") * -1
        rot = gamepad.get_joystick("Rx") * sensitivity_rot

        motors.holonomic(y,x,rot)

while True:
    program.manual()
