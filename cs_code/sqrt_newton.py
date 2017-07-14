def square_root(y, epsilon):
	"""
	uses Newton to compute square root to precision epsilon
	"""
	guess = 1.0
	while abs(guess * guess - y) > epsilon:
		errror = guess * guess - y
		slope = 2.0 * guess  # compute derivitive
		guess = guess - error / slope
	return guess
