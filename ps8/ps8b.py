###########################
# Problem Set 8b: Space Cows 
# Name: Amy Geojo


from ps8b_partition import getPartitions
import time
import operator

#================================
# Part 2: Transporting Space Cows
#================================

# Problem 5
def loadCows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name, weight pairs
    """
    # TODO: Your code here
    cowdata = {}
    data = open(filename, 'r')
    for item in data:
        fields = item.strip().split(',')
        cowdata[fields[0]] = float(fields[1])
    data.close()
    return cowdata

# Problem 6: Greedy Loading (fattest cow first, then next fattest that will still fit)
def greedyTransport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via a greedy heuristic (always choose the heaviest cow to fill the
    remaining space).
    
    Parameters:
    cows - a dictionary of name (string), weight (float) pairs
    limit - weight limit of the spaceship
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    trips = []
    weight = 0.0
    ship = []
    #returns tuple of key,value pairs with higest wt as last element
    cowsCopy = sorted(cows.items(), key = operator.itemgetter(1), reverse = True)
    i = 0
    while i < len(cows):
        if weight + cowsCopy[i][1] <= limit:
            ship.append((cowsCopy[i][0]))   #keep adding cows to 
            weight += cowsCopy[i][1]
            i += 1
        else:
            trips.append(ship)
            ship = []
            weight = 0.0
    trips.append(ship)
    return trips

         
  
#Problem 7: Brute force loading
def bruteForceTransport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.
    
    Parameters:
    cows - a dictionary of name (string), weight (float) pairs
    limit - weight limit of the spaceship
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    best_trips = cows.keys()  #initialize best_trips to # of cows (each cow travels alone)-worst case
    for part in getPartitions(cows):
        current_trips = []
        for lst in part:      #list of cow names; each lst = 1 trip; part = total set of trips
            weight = 0.0
            
            for name in lst:
                weight += cows[name]   #get total wt of cows in lst

            if weight <= limit:
                current_trips.append(lst)  # if wt of cows w/in lst (one of the lists in part) is under wt limit, keep it


        if len(current_trips) == len(part):       #make sure that all lsts in part are valid before checking             
            if len(current_trips) < len(best_trips):  # if current_trips has fewer trips than the stored best_trips, then update best_trips to be current_trips
                best_trips = current_trips

    return best_trips

  
        

##
##[['Maggie', 'Henrietta', 'Lola', 'Oreo', 'Betsy', 'Moo Moo', 'Milkshake', 'Millie', 'Florence', 'Herman']]
##[['Henrietta', 'Lola', 'Oreo', 'Betsy', 'Moo Moo', 'Milkshake', 'Millie', 'Florence', 'Herman'], ['Maggie']]
##[['Maggie', 'Lola', 'Oreo', 'Betsy', 'Moo Moo', 'Milkshake', 'Millie', 'Florence', 'Herman'], ['Henrietta']]
##[['Lola', 'Oreo', 'Betsy', 'Moo Moo', 'Milkshake', 'Millie', 'Florence', 'Herman'], ['Maggie', 'Henrietta']]


##        """each each part is a list of lists; where each list w/in it is one trip of cows;
##        lst (each list in part); check if the weight of  cows in lst is within wt limit
##        it not, discard part altogether;
##        then, check next part;
##        if all lsts within part are w/in wt limit, store it and next time another part meets
##        that criterion, compare the number of lsts within both; whichever has fewer lsts (ie trips)
##        keep that as optimal trip plan
##        """



# Problem 8: Comparing the Loading Algorithms

if __name__ == "__main__":

    """
    Using the data from ps8b_data.txt and the specified weight limit, run your
    greedyTransport and bruteForceTransport functions here. Print out the
    number of trips returned by each method, and how long each method takes
    to run in seconds.
    """
    # Question: How do the results compare? Which ran faster?
    cows = loadCows("ps8b_data.txt")
    
    start = time.time()
    greedy = greedyTransport(cows, 1.0)
    end = time.time()
    greedyTime = end - start



    start = time.time()
    bruteForce = bruteForceTransport(cows, 1.0)
    end = time.time()
    bruteForceTime = end - start





    print "Number of trips for greedy algorithm: " + str(len(greedy))
    print "Greedy algorithm runtime: " + str(greedyTime) + " seconds"
    print "Greedy algorithm runtime: " + str(round(greedyTime*1000,2)) + " milliseconds"

    print "-------------------"

    print "Number of trips for brute force algorithm: " + str(len(bruteForce))
    print "Brute force algorithm runtime: " + str(bruteForceTime) + " seconds"
    print "Brute force algorithm runtime: " + str(round(bruteForceTime*1000,2)) + " milliseconds"
    
    





