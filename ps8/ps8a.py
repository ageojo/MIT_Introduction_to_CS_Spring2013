###########################
# Problem Set 8: Space Cows 
# Name: Amy Geojo


import pylab
import random
#============================
# Part A: Breeding Alien Cows
#============================


# Problem 1: File I/O
def loadData(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated x,y pairs.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    (x, y) - a tuple containing a Pylab array of x values and
             a Pylab array of y values
    """
    # TODO: Your code here
    data = open(filename, 'r')
    x = []
    y = []
    for item in data:
        fields = item.strip().split(',')   #each line of file has 2 #s; csv file
        x.append(float(fields[0]))
        y.append(float(fields[1]))

    data.close()
    return (pylab.array(x), pylab.array(y))      #convert list to array
        


# Problem 2a: Curve Fitting: Finding a polynomial fit
def polyFit(x, y, degree):
    """
    Find the best fit polynomial curve of the specified degree for the data
    contained in x and y and return the coefficients for the best fit
    polynomial curve of the given degree using the original set of x values.

    Parameters:
    x - a Pylab array of x values
    y - a Pylab array of y values
    degree - the degree of the desired best fit polynomial

    Returns:
    a Pylab array of coefficients for the polynomial fit function of the
    specified degree, corresponding to the input domain x.
    """
    # TODO: Your code here
    return pylab.polyfit(x, y, degree)


# Problem 2b: Curve Fitting: Finding an exponential fit
def expFit(x, y):
    """
    Find the best fit exponential curve's coefficients for the data contained
    in x and y.

    Parameters:
    x - a Pylab array of x values
    y - a Pylab array of y values

    Returns:
    a Pylab array of coefficients for the exponential fit function
    corresponding to the input domain x.
    """
    # TODO: Your code here
    logY = pylab.log2(y)
    return polyFit(x, logY, 1)


# Problem 3: Evaluating regression functions
def rSquare(measured, estimated):
    """
    Calculate the R-squared error term.

    Parameters:
    measured - one dimensional array of measured values
    estimate - one dimensional array of predicted values

    Returns: the R-squared error term
    """
    assert len(measured) == len(estimated)
    EE = ((estimated - measured)**2).sum()
    mMean = measured.sum()/float(len(measured))
    MV = ((mMean - measured)**2).sum()
    return 1 - EE/MV

##############################

def LinearCoef(data):
    """
    Data is a file with 2 arrays of
    x and corresponding y values.
    Returns coefficients a and b for
    linear function ax + b.
    """
    return polyFit(data[0], data[1], 1)

def QuadraticCoef(data):
    return polyFit(data[0], data[1], 2)

    
def QuarticCoef(data):
    return polyFit(data[0], data[1], 4)


def ExponCoef(data):
    return expFit(data[0], data[1])



def LinearEstY(data1, data2):  #creates model from data 1; extends by estY values based on that model to other data sets
    a, b = LinearCoef(data1)
    return a*data2[0] + b # returns estimated Y values using x values from data2 = data2[0] (but fx from data1)
    

def QuadraticEstY(data1, data2):
    a, b, c = QuadraticCoef(data1)
    return a*(data2[0]**2) + b*data2[0] + c


def QuarticEstY(data1, data2):
    a, b, c, d, e = QuarticCoef(data1)
    return a*(data2[0]**4) + b*(data2[0]**3) + c*(data2[0]**2) + d*data2[0] + e


def ExponEstY(data1, data2):
    """
    Takes 2 data sets, each consisting of 2 arrays.
    Returns estimated y values for data2
    based on exponential curve fit on data1.
    """
    a, b = ExponCoef(data1)
    return 2**(a*data2[0] + b)
    


def plotData(fcn, data2, title):  #dont need to include data1, data2? b/c those should be included in the fcn?
    """
    fcn: a function that takes 2 data sets and returns estimated y values for
    the 2nd data set based on a model fit to the first data set.
    Returns a plot with data 2 as a scatterplot and the curve-overlaid
    """

    estYvals = fcn  #returns est y values for data2 (based on curve for data1)
 #   pylab.subplot(2, 2, n)
    pylab.plot(data2[0], estYvals, label = title + "; R2= " + str(round(rSquare(data2[1], estYvals), 2)))
    pylab.plot(data2[0], data2[1], 'ro')
    pylab.title('Change in cow population')
    pylab.xlabel('Day')
    pylab.ylabel('# of cows')
    pylab.legend(loc = 'best')
    pylab.savefig(title)
    pylab.show()
    


  

##def fitData(data):
##    xVals, yVals = data[0], data[1]
##    pylab.figure(1)
##    pylab.plot(xVals, yVals, 'bo')
##    pylab.savefig('Scatter Plot')
##    
##    a, b = polyFit(xVals, yVals, 1)
##    estYvals = a*xVals + b
##    pylab.figure(2)
##    pylab.plot(xVals, estYvals, label = 'Linear fit, ' + 'R2= ' + str(round(rSquare(yVals, estYvals), 2)))
##    pylab.savefig('Linear Fit')
##
##    a, b, c = polyFit(xVals, yVals, 2)
##    estYvals = a*(xVals**2) + b*xVals + c
##    pylab.figure(3)
##    pylab.plot(xVals, estYvals, label = 'Quadratic fit ' + 'R2= ' + str(round(rSquare(yVals, estYvals), 2)))
##    pylab.savefig('Quadratic fit')
##
##    a, b, c, d, e = polyFit(xVals, yVals, 4)
##    estYvals = a*(xVals**4) + b*(xVals**3) + c*(xVals**2) + d*xVals + e
##    pylab.figure(4)
##    pylab.plot(xVals, estYvals, label = 'Quartic fit ' + 'R2= ' + str(round(rSquare(yVals, estYvals), 2)))
##    pylab.savefig('Quartic fit')
##    pylab.legend(loc = 'best')
##    
##    a, b = expFit(xVals, yVals)
##    estYvals = b * 2**(a*xVals)
##    pylab.figure(5)
##    pylab.plot(xVals, estYvals, label = 'Exponential fit')
##    pylab.savefig('Exponential fit')
##    pylab.show()
    



    
#======================
# TESTING CODE
#======================
def main():
    # Problem 1
    data1 = loadData('ps8a_data1.txt') # TODO: your code here
    data2 = loadData('ps8a_data2.txt') # TODO: your code here
    data3 = loadData('ps8a_data3.txt') # TODO: your code here
 #   print data1
    
    # Checks for Problem 1
    assert all([all([len(xy) == 25 for xy in data]) for data in [data1, data2]]), \
        "Error loading data from files; number of terms does not match expected"

    assert all( [len(xy) == 100 for xy in data3]), \
        "Error loading data from files; number of terms does not match expected"

##
##
## Graphs for DataSet 1
    # graph 1/12 - dataSet 1, linear; compute rSquare to see how well model fits data
 #   pylab.subplot(2,2,1)
    plotData(LinearEstY(data1, data1), data1, "Data 1: Linear model")
    
    # graph 2 - dataSet 1, quadratic
 #   pylab.subplot(2,2,2)
    plotData(QuadraticEstY(data1, data1), data1,  "Data 1: Quadratic model")

    # graph 3- dataSet 1, quartic
#    pylab.subplot(2,2,3)
    plotData(QuarticEstY(data1, data1), data1, "Data 1: Quartic model")

    #graph 4 - dataset 1, exponential
#    pylab.subplot(2,2,4)
    plotData(ExponEstY(data1, data1), data1, "Data 1: Exponential model")


## Graphs for DataSet 2
    # graph 5 - dataSet 2, linear; compute rSquare to see how well model fits data
    plotData(LinearEstY(data1, data2), data2, "Data 2: Linear model")
    
    # graph 6 - dataSet 2, quadratic
    plotData(QuadraticEstY(data1, data2), data2,  "Data 2: Quadratic model")

    # graph 7- dataSet 2, quartic 
    plotData(QuarticEstY(data1, data2), data2, "Data 2: Quartic model")

    #graph 8 - dataset 2, exponential
    plotData(ExponEstY(data1, data2), data2, "Data 2: Exponential model")



## Graphs for DataSet 3
    # graph 9 - dataSet 3, linear; compute rSquare to see how well model fits data
    plotData(LinearEstY(data1, data3), data3, "Data 3: Linear model")
    
    # graph 10 - dataSet 3, quadratic
    plotData(QuadraticEstY(data1, data3), data3,  "Data 3: Quadratic model")

    # graph 11 - dataSet 3, quartic 
    plotData(QuarticEstY(data1, data3), data3, "Data 3: Quartic model")

    #graph 12 - dataset 3, exponential
    plotData(ExponEstY(data1, data3), data3, "Data 3: Exponential model")




### Predicted # of cows after 200 days based on exponential coeff from data1, 2, and 3
##    a, b, = a, b = ExponCoef(data1)
###    print a, b
##    x = 200 #200 days
##    cows200days = 2**(a*x + b)
##    print "predicted # cows after 200 days from data1: " + str(round(cows200days, 2))
##
###    print "______________________"
##    
##    a, b, = a, b = ExponCoef(data2)
##    x = 200 #200 days
##    cows200days = 2**(a*x + b)
##    print "predicted # cows after 200 days from data2: " + str(round(cows200days, 2))
##
###    print "______________________"
##
##    
##    a, b = ExponCoef(data3)
##    x = 200 #200 days
##    cows200days = 2**(a*x + b)
## #   [ 0.04990773  7.72134362] #a, b
###    2**(a*data2[0] + b)
##    print "predicted # cows after 200 days from data3: " + str(round(cows200days, 2))
##





    
if __name__ == "__main__":
    main()
    
