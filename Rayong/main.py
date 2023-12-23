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
encode_feeder = encoder_motor_class("M5", "INDEX1")

#Pin grabber Servo
servo_grabber_main = smartservo_class("M6", "INDEX1")
servo_grabber_sub = smartservo_class("M6", "INDEX2")

#Sensitivity
BL_spd = 25
sensitivity_rot = 0.7
sensitivity_RY = -0.4
box_grab_state = False
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

class useful_function:
    def Brushless_spd_mode():
        global BL_spd
        if gamepad.is_key_pressed("R2"):
            if BL_spd == 25:
                BL_spd = 70
            elif BL_spd == 70:
                BL_spd = 0
            elif BL_spd == 0:
                BL_spd = 25
            else:
                BL_spd = 25
            pass
            while gamepad.is_key_pressed("R2"):
                pass
        return BL_spd

    def arm_control():
        #Open and close the Cube Grabber
        if gamepad.is_key_pressed("Right"):
            power_expand_board.set_power("DC1", 100)
        elif gamepad.is_key_pressed("Left"):
            power_expand_board.set_power("DC1", -100)
        else:
            power_expand_board.stop("DC1")

        #move the arm up and down
        if gamepad.is_key_pressed("Up"):
            power_expand_board.set_power("DC2", 100)
        elif gamepad.is_key_pressed("Down"):
            power_expand_board.set_power("DC2", -100)
        else:
            power_expand_board.stop("DC2")

        useful_function.box_grabber_control()

    def box_grabber_control():
        global box_grab_state
        servo_grabber_main.set_power(gamepad.get_joystick("Ry") * sensitivity_RY)

        #open and cloes grabber
        if gamepad.is_key_pressed("N1"):
            if box_grab_state == True:
                servo_grabber_sub.move_to(-17, 30)    
                box_grab_state = False
                while gamepad.is_key_pressed("N1"):
                    pass

            elif box_grab_state == False:
                servo_grabber_sub.move_to(45, 30)
                box_grab_state = True
                while gamepad.is_key_pressed("N1"):
                    pass

     # new shortcut key N2,N4        
        if gamepad.is_key_pressed("N2"):
            if box_grab_state == True:
                servo_grabber_main.move_to (90,30)      
                box_grab_state = False
                while gamepad.is_key_pressed("N2"):
                    pass
            elif box-grab_state == False:
                servo_grabber_main.move_to(0,30)
                box_grab_state = False
                while gamepad.is_key_pressed("N2")
                    pass
            
        if gamepad.is_key_pressed("N4"):
            if box_grab_state == False:
                servo_grabber_sub.move_to(-12, 30)
                box_grab_state = True
                while gamepad.is_key_pressed("N4"):
                    pass

            elif box_grab_state == True:
                servo_grabber_sub.move_to(45, 30)
                box_grab_state = False
                while gamepad.is_key_pressed("N4"):
                    pass
            
            
        


        
    
class program:

    #manual program
    def manual():
        x = gamepad.get_joystick("Lx")
        y = gamepad.get_joystick("Ly") * -1
        rot = gamepad.get_joystick("Rx") * sensitivity_rot

        #movement
        motors.holonomic(y,x,rot)

        #feel ball
        if gamepad.is_key_pressed("L1"):
            encode_feeder.set_power(100)
        elif gamepad.is_key_pressed("R1"):
            encode_feeder.set_power(-100)
        else:
            encode_feeder.set_power(0)

        #check for change brushless motor spd
        useful_function.Brushless_spd_mode()
        useful_function.arm_control()


while True:
    program.manual()
