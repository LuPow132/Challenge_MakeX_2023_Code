import math

degToRad = 0.0174
sin30 = math.sin(30 * degToRad)
cos30 = math.cos(30 * degToRad)

spd = 100
theta = 270
omega = 0

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def holonomic(spd,theta,omega):
    thetaRad = theta * degToRad
    vx = spd * math.cos(thetaRad)
    vy = spd * math.sin(thetaRad)
    rot = omega / degToRad
    print(f'VX:{vx} VY:{vy} rot:{rot}')

    EFL = round(vy * cos30 - vx * sin30 + omega)
    EFR = round(vy * cos30 - vx * sin30 + omega)
    EREAR = round(vx + omega)

    print(f'{EFL}\t\t{EFR}\n\n\n\n\t{EREAR}')

# void holonomic(float spd, float theta, float omega) {
#   thetaRad = theta * degToRad;
#   vx = spd * cos(thetaRad);
#   vy = spd * sin(thetaRad);
#   spd1 =   vy * cos30 - vx * sin30 + omega;
#   spd2 = - vy * cos30 - vx * sin30 + omega;
#   spd3 =   vx + omega;
#   wheel(spd1, spd2, spd3);
# }

holonomic(spd,theta,omega)
