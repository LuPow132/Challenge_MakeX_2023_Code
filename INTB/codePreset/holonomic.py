import math

degToRad = 0.0174


spd = 0
theta = 0
omega = 0

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def holonomic(spd,theta,omega):
  thetaRad = theta * degToRad
  vx = round(spd * math.cos(thetaRad))
  vy = round(spd * math.sin(thetaRad))
  rot = omega / degToRad
  print(f'VX:{vx} VY:{vy} rot:{rot}')

  EFl = constrain((vx - vy) - rot, -100, 100)
  EFr = -constrain((vx + vy) + rot, -100, 100) #-
  ERl = constrain((vx + vy) - rot, -100, 100)
  ERr = -constrain((vx - vy) + rot, -100, 100) #-

  print(f'{EFl}\t{EFr}\n\n\n{ERl}\t{ERr}')

holonomic(spd,theta,omega)
