#import library
from mbuild import power_expand_board
from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild.smartservo import smartservo_class
from mbuild import gamepad
from mbuild import power_manage_module
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild.led_matrix import led_matrix_class
import math
import time
import novapi

#-----Configuration-----#

#Assign each encode ,servo motor ,camera

#drive encode motor
#encode_fl = encoder_motor_class("M1", "INDEX1")
#encode_fr = encoder_motor_class("M2", "INDEX1")
#encode_rl = encoder_motor_class("M3", "INDEX1")
#encode_rr = encoder_motor_class("M4", "INDEX1")
encode_fl = encoder_motor_class("M4", "INDEX1")
encode_fr = encoder_motor_class("M3", "INDEX1")
encode_rl = encoder_motor_class("M2", "INDEX1")
encode_rr = encoder_motor_class("M1", "INDEX1")


encode_feeder = encoder_motor_class("M5", "INDEX1")

# DC1 = ball check
# DC2 = arm up/down
# DC3 = feed barrel

#Pin grabber Servo
servo_grabber_main = smartservo_class("M6", "INDEX1")  
servo_grabber_sub = smartservo_class("M6", "INDEX2")

led_matrix_1 = led_matrix_class("PORT2", "INDEX1")

#Sensitivity
BL_spd = 0
sensitivity_rot = 0.5
sensitivity_RY = 0.4
box_grab_state = False
ball_flicker = True
side = True
current_overload_loop = False

#PID
head_Kp = 0.8
head_Ki = 0.5
head_Kd = 0.5
head_d = 0.0
head_i = 0.0
head_w = 0.0
head_pError = 0.0
heading_sensitivity = 1

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
        if gamepad.is_key_pressed("R_Thumb"):
            if BL_spd == 70:
                BL_spd = 100
            elif BL_spd == 100:
                BL_spd = 0
            elif BL_spd == 0:
                BL_spd = 70
            else:
                BL_spd = 70
            pass
            while gamepad.is_key_pressed("R_Thumb"):
                pass
        return BL_spd

    def toggle_function(buttons, variable): # Test this function
        
        if gamepad.is_key_pressed(buttons):
            if variable == True:
                variable = False
            else:
                variable = True
            pass
            while gamepad.is_key_pressed(buttons):
                pass
        
        return variable
    
    def constrain(v, mn, mx):
        if v < mn : return mn
        if v > mx : return mx
        return v
        


    def arm_control():
        #move the arm up and down   # Add for encoder motor
        if gamepad.is_key_pressed("Up"):
          #  encode_updown.set_power(100)
            power_expand_board.set_power("DC2", 100)
        elif gamepad.is_key_pressed("Down"):
           # encode_updown.set_power(-100)
            power_expand_board.set_power("DC2", -100)
        else:
          #  encode_updown.set_power(0)
            power_expand_board.stop("DC2")


        #call for sub arm (pin arm)
        useful_function.box_grabber_control()


    def box_grabber_control():
        global box_grab_state
        servo_grabber_main.set_power( -1 * gamepad.get_joystick("Ry") * 0.2)
        #open and cloes grabber
        if gamepad.is_key_pressed("N1"):
            while gamepad.is_key_pressed("N1"):
                # DO SOMETHING
                pass    
            current_servo = servo_grabber_sub.get_value("current")
            while current_servo < 1100:
                servo_grabber_sub.set_power(-20)
                current_servo = servo_grabber_sub.get_value("current")
            servo_grabber_sub.set_power(0)
     
           # new shortcut key N2,N3,N4  
        if gamepad.is_key_pressed("N2"):
           
                servo_grabber_main.move_to(45, 30)   
                time.sleep(0.5)
              
        if gamepad.is_key_pressed("N3"):   
                servo_grabber_main.move_to(147, 30)  
                time.sleep(0.5)
                   
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
        
    def gun_control():
        if gamepad.is_key_pressed("R2"):
            encode_feeder.set_power(-100)
        elif gamepad.is_key_pressed("L2"):
            encode_feeder.set_power(100)
        else:
            encode_feeder.set_power(0)
        #feel ball

        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC3", 100)
        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("DC3", -100)
        else:
            power_expand_board.stop("DC3")
    
    def heading(x,y,heading_rot):
        
        global head_i,head_w,head_Kd,head_Kp,head_error,head_pError

        current_rot = novapi.get_yaw()

        head_error = heading_rot - current_rot
        head_i = head_i - head_error
        head_i = useful_function.constrain(head_i,-180,180)
        head_d = head_error - head_pError
        head_w = (head_error * head_Kp) + (head_i * head_Ki) + (head_d * head_Kd)
        head_w = useful_function.constrain(head_w *  heading_sensitivity,-100,100)
        led_matrix_1.show(head_w, wait = False)


        motors.holonomic(y,x,head_w)

        head_pError = head_error
class program:

    #manual program
    def manual():
        global gun_mode,side,ball_flicker

        side = useful_function.toggle_function("≡",side)
        ball_flicker = useful_function.toggle_function("+",ball_flicker)

        if side == True:
            x = gamepad.get_joystick("Lx")
            y = gamepad.get_joystick("Ly") * -1 * sensitivity_RY
        else:
            x = gamepad.get_joystick("Ly")
            y = gamepad.get_joystick("Lx")

        rot = gamepad.get_joystick("Rx") * sensitivity_rot * sensitivity_RY

        #movement
        motors.holonomic(y,x,rot)

        if ball_flicker == True:
            power_expand_board.set_power("DC1", -100)
        else:
            power_expand_board.stop("DC1")

        #check for change brushless motor spd
        useful_function.Brushless_spd_mode()
        power_expand_board.set_power("BL1", BL_spd)
        power_expand_board.set_power("BL2", BL_spd)

        useful_function.gun_control()
        useful_function.arm_control()
            
    def auto():
        useful_function.heading(0,50,0)
        

novapi.reset_rotation("z")
while True:
    program.auto()

    
