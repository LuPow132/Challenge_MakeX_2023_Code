import math

degToRad = 0.0174
sin30 = math.sin(30 * degToRad)
cos30 = math.cos(30 * degToRad)

spd = 0
theta = 0
omega = 0

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def holonomic(spd,theta,omega):
    thetaRad = theta * degToRad
    vx = spd * math.cos(thetaRad)
    vy = spd * math.sin(thetaRad)
    rot = constrain(omega / degToRad,-100,100)
    print(f'Vx:{round(vx)}, Vy:{round(vy)}, Rot:{round(rot)}')

# void holonomic(float spd, float theta, float omega) {
#   thetaRad = theta * degToRad;
#   vx = spd * cos(thetaRad);
#   vy = spd * sin(thetaRad);
#   spd1 =   vy * cos30 - vx * sin30 + omega;
#   spd2 = - vy * cos30 - vx * sin30 + omega;
#   spd3 =   vx + omega;
#   wheel(spd1, spd2, spd3);
# }

#holonomic(spd,theta,omega)

for i in range(-100,100):
    print(f'{i}---------------')
    holonomic(spd,theta,i)
