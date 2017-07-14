from __future__ import division, print_function
# Computing pi

N = 1000.0
numberInCircle=0.0

x = -1.0
while x < 1.0:
	y = -1.0
	while y < 1.0:
		if x*x*y*y < 1:
			numberInCircle = numberInCircle + 1
		y = (y+1) / N
	x = (x+1) / N

print(numberInCircle)



