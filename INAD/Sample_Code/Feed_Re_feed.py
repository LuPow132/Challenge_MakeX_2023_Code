# codes make you happy
import novapi
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild import gamepad
from mbuild import power_expand_board

# initialize variables
Exit_Loop1 = 0

# new class
distance_sensor_1 = ranging_sensor_class("PORT2", "INDEX1")

novapi.reset_timer()
Exit_Loop1 = 0
while not (Exit_Loop1 == 1):
    time.sleep(0.001)
    if gamepad.is_key_pressed("R2"):
        Exit_Loop1 = 1

    else:
        if distance_sensor_1.get_distance() < 6:
            Exit_Loop1 = 1

        else:
            if novapi.timer() > 5:
                power_expand_board.set_power("DC1", -100)
                power_expand_board.set_power("DC2", -70)
                time.sleep(1.5)
                novapi.reset_timer()

            else:
                power_expand_board.set_power("DC1", 100)
                power_expand_board.set_power("DC2", 70)

power_expand_board.stop("DC1")
power_expand_board.stop("DC2")
power_expand_board.set_power("BL1", 50)
power_expand_board.set_power("BL2", 50)

