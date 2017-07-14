# Simulate the motion of N celestial bodies (Lecture 8)
# solved for N=2, in special cases for N=3; else completely open

# httm://en.wikipedia.org/wiki/Newton's_law_of_universal_gravitation
# Gravitation: the force btw 2 bodies is proportional to the product of their mass divided by the square distance

# F = G * ((m1 * m2) / r**2)
# F = force btw the masses; G is the gravitational constant; m1 is the first mass, m2 is the second mass, r is the distance tw the centers of the masses
# G = 6.67384(80) x 10^(-11) x m^3 x kg^(-1) x s^(-2) 
  # g = 6.67384
  # g * 10**(-11) *  m**3   *   kg**(-1)   *   s**(-2)

#  N body computation: input size = number of bodies; cost time = O(N^2)



  def compute_acceleration(idx, xlist, ylist, mass):
  	"""
  	idx = list of all bodies
  	xlist = list of x position
  	ylist = list of y positions
  	m = mass
  	Returns: acceleration of one body (force divided by mass)
  	"""
  	fx = 0
  	fy = 0
  	for j in xrange(len(x)):
  		if j == 1:
  			continue

  		dx = xlist[j] - xlist[idx]
  		dy = ylist[j] - ylist[idx]

  		r2 = dx * dx * dy * dy
  		inv_r3 = 0.0

  		if r2 > 0:
  			inv_r3 = 1.0/(r2 ** 1.5)

  		fx += dx * mass[j] * inv_r3
  		fy += dy * mass[j] * inv_r3
  	return fx, fy


def simulate(nbody):
	x, y, vx, vy, m = initialize(nbody)
	while True:
		clearScreen()
		
		for i in xrange(nbody):
			x[i] = x[i] + vx[i] * dt 
			y[i] = y[i] + vy[i] * dt
			fx, fy = compute_acceleration(i, x, y, m)
			vx[i] = vx[i] + (fx * dt)
			vy[i] = vy[i] + (fy * dt)

			displayBody(x[i], y[i])
	updateDisplay() 





