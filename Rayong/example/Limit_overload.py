import novapi
from mbuild.led_matrix import led_matrix_class
from mbuild.smartservo import smartservo_class
from mbuild import gamepad

# new class
led_matrix_1 = led_matrix_class("PORT2", "INDEX1")
smartservo_1 = smartservo_class("M1", "INDEX1")
smartservo_2 = smartservo_class("M1", "INDEX2")

while True:
    if gamepad.is_key_pressed("N1"):
        while not (smartservo_2.get_value("current") > 1400):
            smartservo_2.set_power(-100)

        smartservo_2.set_power(0)
        while not not gamepad.is_key_pressed("N1"):
            # DO SOMETHING
            pass
