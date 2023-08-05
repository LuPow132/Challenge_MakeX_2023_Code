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


#------PID control------#

head_Kp = 0.16
head_Ki = 0.2
head_Kd = 0.5 

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
degToRad = 0.0174
sin30 = math.sin(30 * degToRad)
cos30 = math.cos(30 * degToRad)
head_error,head_pError,head_w,head_d,head_i = 0

#Some function that novapi too lazy to put it in#

#Value, Min Value, Max Value
def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

#Class that get all novapi inside sensor info
class novapi_info():
    def get_Yaw():
        global pvYaw
        pvYaw = novapi.get_yaw()
        return pvYaw
    
    def reset_Yaw():
        novapi.reset_rotation("z")

    def reset_timer():
        novapi.reset_timer()
        #To get time you can just use "novapi.timer()" which return time in seconds



#Class that management the motor job things
class motor:
    def drive(spd1,spd2,spd3):
        encode_FL.set_power(spd1)
        encode_FR.set_power(spd2)
        encode_Rear.set_power(spd3)

    #Give power and angle and rot to it
    def holonomic(spd,theta,omega):
        thetaRad = theta * degToRad
        vx = spd * math.cos(thetaRad)
        vy = spd * math.sin(thetaRad)
        rot = omega / degToRad

        EFL = round(vy * cos30 - vx * sin30 + omega)
        EFR = round(vy * cos30 - vx * sin30 + omega)
        EREAR = round(vx + omega)

        motor.drive(EFL,EFR,EREAR)

    #holonomic but can keep angle where to heading
    #spd = speed   theata = angle you want to go  spYaw = angle you wanna keep
    def heading(spd,theta,spYaw):
        #Get Yaw from novapi
        novapi_info.get_Yaw()

        head_error = spYaw - pvYaw
        head_i = head_i  + head_error
        head_i = constrain(head_i ,-180,180)
        head_d =  head_error - head_pError
        head_w = (head_error * head_Kp) + (head_i * head_Ki) + (head_d * head_Kd)
        head_w = constrain(head_w ,-100,100)

        motor.holonomic(spd, theta, head_w)
        head_pError = head_error

class challenge_program():
    #Give LX,LY,RX input to this function
    def manual_controll(vx,vy,rot):
        EFL = round(vy * cos30 - vx * sin30 + rot)
        EFR = round(vy * cos30 - vx * sin30 + rot)
        EREAR = round(vx + rot)

        motor.drive(EFL,EFR,EREAR)

    def toggle_function(buttons, variable): # Toggle function
        if gamepad.is_key_pressed(buttons):
            if variable == True:
                variable = False
            else:
                variable = True
            pass
            while gamepad.is_key_pressed(buttons):
                pass
        
        return variable
    
    def Brushless_spd_mode():
        global BL_spd
        if gamepad.is_key_pressed("R2"):
            if BL_spd == 17:
                BL_spd = 70
            elif BL_spd == 70:
                BL_spd = 0
            elif BL_spd == 0:
                BL_spd = 17
            else:
                BL_spd = 17
            pass
            while gamepad.is_key_pressed("R2"):
                pass
        return BL_spd
    
    def manual():
        pass

    def auto():
        pass

class start_with():
    def joystick():
    
        mode = "select" # select = selectmenu; program = run; anything else = ?

        while mode == "select":

            if gamepad.is_key_pressed("N2"):
                mode = "auto"
                challenge_program.auto_program()

            if gamepad.is_key_pressed("N4"):
                mode = "manual"
                while True:
                    challenge_program.manual()


    def power_management():
        if power_manage_module.is_auto_mode():
            pass
            #auto code here
        else:
            pass
            #manual code here


