# missing simpleplot.py

# vx = v * cos(theta)
# vy = v * sin(theta)
#where x and y refer to the x and y axis; v= velocity

# change in x = vx * (change in t)
# change in y = vy * (change in t) + (0.5g) * (change in t)**2
# change in vy = g * (change in t)

# (x,y) coordinates indicating location of angry nerd

import math
import simpleplot as sp 

g = -9.8
dt = 0.01

x, y = 0.1, 0.1
v = 25.0
ang = 30.0

vx = v * math.cos((ang/180.0) * math.pi)
vy = v * math.sin((ang/180.0) * math.pi)

while y > 0.0:
	x = x + vx * dt
	y = y + vy * dt + g * dt * (dt/2)
	vy = vy + g*dt
	sp.plotTrajectory((x,y))

print(x)
sp.doAnimation()