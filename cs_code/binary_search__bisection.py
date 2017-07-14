from __future__ import division, print_function

def binary_search(f, goal, low, high, epsilon):
	"""returns the value such that f(value) = goal within epsiolon"""
	mid = (low + high) / 2.0
	value = f(mid)
	while abs(value - goal) > epsilon:
		if (value < goal):
			low = mid
		else:
			high = mid
		mid = (low + high) / 2.0
		value = f(mid)
	return mid
	

