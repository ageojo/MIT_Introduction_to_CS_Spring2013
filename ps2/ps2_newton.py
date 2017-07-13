# 6.00 Problem Set 2
# Problem Set 2
# Name: Amy C. Geojo




# Successive Approximation: Newton's Method
#

def evaluate_poly(poly, x):
    """
    Computes the value of a polynomial function at given value x. Returns that
    value as a float.

    Example:
    >>> poly = [0.0, 0.0, 5.0, 9.3, 7.0]    # f(x) = 5x^2 + 9.3x^3 + 7x^4 
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 5(-13)^2 + 9.3(-13)^3 + 7(-13)^4 
    180339.9

    poly: list of numbers, length > 0
    x: number
    returns: float
    """
    # FILL IN YOUR CODE HERE ...
    
    lenghtpoly =len(poly)
    s = []
    for i in range(lenghtpoly):
        ans = (x**i)*poly[i]
        s.append(float(ans))
        polyvalue = sum(s)
    return polyvalue


#########################################

def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function as a list of
    floats. If the derivative is 0, returns [0.0].

    Example:
    >>> poly = [-13.39, 0.0, 17.5, 3.0, 1.0]    # - 13.39 + 17.5x^2 + 3x^3 + x^4
    >>> print compute_deriv(poly)        # 35^x + 9x^2 + 4x^3
    [0.0, 35.0, 9.0, 4.0]

    poly: list of numbers, length > 0
    returns: list of numbers (floats)
    """
    # FILL IN YOUR CODE HERE ...
    lenghtpoly =len(poly)
    derivative = []
    for i in range(lenghtpoly):
        coefficient = i*poly[i]
        derivative.append(abs(float(coefficient)))
    derivative.pop(0)
    return derivative



#########################################   

def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a list containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = [-13.39, 0.0, 17.5, 3.0, 1.0]    # - 13.39 + 17.5x^2 + 3x^3 + x^4
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    [0.80679075379635201, 8]
    >>> poly = [1, 9, 8]
    >>> x_0 = -3
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    [-1.0000079170005467, 6]

    poly: list of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: list [float, int]
    """
    # FILL IN YOUR CODE HERE ... 

    iteration = 1
    while abs(evaluate_poly(poly, x_0)) >= epsilon:
        x_0 = float(x_0 - ((evaluate_poly(poly, x_0))/evaluate_poly(compute_deriv(poly), x_0)))
        iteration = iteration + 1
        Root_And_Iteration = [x_0, iteration]
    return Root_And_Iteration





##print evaluate_poly([0.0, 0.0, 5.0, 9.3, 7.0],-13)
##print evaluate_poly([1,2,3], 2)
##
##print compute_deriv([1,2,3])
##print compute_deriv([-13.39, 0.0, 17.5, 3.0, 1.0])
##
##
##poly = [-13.39, 0.0, 17.5, 3.0, 1.0]
##x_0 = 0.1
##epsilon= 0.0001
##print compute_root(poly, x_0, epsilon)
##
##poly = [1,9,8]
##x_0 = -3
##print compute_root(poly, x_0, epsilon)
