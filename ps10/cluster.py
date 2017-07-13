# 6.00 Problem Set 10
# cluster.py
# Classes and code for k-means clustering

# ***** READ THROUGH AND UNDERSTAND THIS FILE!! ***** #


import pylab, random, string, copy, math

class Point(object):
    '''
    Represents a data point
    '''
    
    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalizedAttrs = originalAttrs

        if normalizedAttrs != None:
            self.normAttrs = normalizedAttrs

        else:
            # If normalized attributes aren't provided, just use the originals.
            self.normAttrs = originalAttrs

    def dimensionality(self):
        """Returns the dimensionality of the point"""
        return len(self.normAttrs)

    def getAttrs(self):
        """Returns the normalized attributes"""
        return self.normAttrs

    def getAttr(self, dimension):
        """
        Returns the value of this point's normialized attribute
        for the given dimension.
        """
        return self.getAttrs()[dimension]

    def getOriginalAttrs(self):
        """Returns the unnormalized attributes"""
        return self.unNormalizedAttrs

    def getOriginalAttr(self, dimension):
        """
        Returns the value of this point's unnormialized attribute
        for the given dimension.
        """
        return self.getOriginalAttrs()[dimension]

    def distance(self, other):
        """Returns Euclidean distance metric between self and other"""
        difference = self.normAttrs - other.normAttrs 
        return sum(difference * difference) ** 0.5

    def getName(self):
        return self.name

    def toStr(self):
        return self.name

    def __str__(self):
        return self.name

class Song(Point):
    # Associate thirteen variable names with the numbers 0 - 12 so we can
    # quickly access the feature vector.
    # Refer to these variables as eg "Song.Loudness"
    (ArtistFamiliarity, ArtistHotness, ArtistLatitude, ArtistLongitude,
     Duration, FadeInEnd, FadeOutStart, Loudness, SampleRate, SongHotness, Tempo,
     TimeSignature, Year) = tuple(range(13))

    # Make a weights vector as a class variable (or 'static variable')
    # for the entire Song class. The feature vector is initialized to
    # give a weight of 1.0 to all 13 dimensions
    weights = pylab.array([1.0] * 13)

    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        Point.__init__(self, name, originalAttrs, normalizedAttrs)

    @staticmethod
    def equal_weights(weight):
        '''
        Sets the weight of every dimension to weight.
        '''
        Song.weights = pylab.array([float(weight)] * 13)

    @staticmethod
    def set_weight(dimension, value):
        '''
        Sets the weight of one dimension of the feature vector to
        the provided value.

        dimension should be a variable name - one of: ArtistFamiliarity,
        ArtistHotness, ArtistLatitude, Duration, etc.
        '''
        Song.weights[dimension] = float(value)

    @staticmethod
    def get_weight(dimension):
        '''
        Returns the weight of one dimension of the feature vector.

        dimension should be a variable name - one of: ArtistFamiliarity,
        ArtistHotness, ArtistLatitude, Duration, etc.
        '''
        return Song.weights[dimension]

    def distance(self, other):
        '''
        Overrides Point.distance to use the weights feature vector to
        decide the significance of each dimension.
        '''
        difference = self.getAttrs() - other.getAttrs()
        return sum(self.weights * difference * difference) ** 0.5
    
class Cluster(object):
    """Represents a cluster"""

    def __init__(self, points, pointType):
        """
        points: a list of Point or Point subclass type objects
        pointType: the type (class name) of the points
        """
        self.points = points
        self.pointType = pointType
        self.centroid = None
        if len(points) > 0:
            # centroid is an instance of pointType
            self.centroid = self.computeCentroid()
    
    def getCentroid(self):
        """Returns the centroid of the cluster"""
        return self.centroid

    def computeCentroid(self):
        """Computes the centroid of the cluster"""
        dim = self.points[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        #the meanPoint is the center of mass of the cluster
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points)))
        return meanPoint


    def update(self, points):
        """
        Replaces the points in the cluster with new points,
        computes the new centroid, and returns the distance 
        between the old and the new centroids.
        """
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)      #distance() from point or song class?
        else:
            return 0.0

    def getPoints(self):
        '''
        Simply returns all the points in this cluster.
        '''
        return self.points

    def contains(self, name):
        """
        Returns whether the point called name is in the cluster.
        """
        for p in self.points:
            if p.getName() == name:
                return True
        return False

    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]

    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]


def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).
    l: The list to split
    p: The probability that an element of l will be in the first partition
    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []   
    l2 = []   
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)

def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = True):
    """
    Computes the k-means clusters
    points: a list of points
    k: the number of clusters
    cutoff: the maximum distance between the new centroids and the old
        centroids below which the iteration can stop (because the clusters
        are stable enough)
    pointType: the class name of the points
    minIters: minimum number of iterations
    maxIters: maximum number of iterations
    return: a list of k clusters and the diameter of the least coherent cluster 
    """
    

    initialCentroids = random.sample(points, k)
    clusters = [Cluster([c], pointType) for c in initialCentroids]

    count = 0
    maxChange = cutoff

    while (maxChange >= cutoff and count < maxIters) or count < minIters:
        newClusters = []
        for i in range(k):
            newClusters.append([])
            
 #       newClusters = [None]*k
         
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(k):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i

            #add p to list of points for appropriate cluster
            newClusters[index].append(p)


        #update each cluster and record change in centroid
            maxChange = 0.0
            for i in range(k):
                change = clusters[i].update(newClusters[i])
                maxChange = max(maxChange, change)

            count += 1


        # calculate diameter of least coherent cluster
        maxDist = 0.0
        for c in clusters:
            for p in c.getPoints():
                if p.distance(c.getCentroid()) > maxDist:
                    maxDist = p.distance(c.getCentroid())

        return clusters, maxDist




 
  
        
        
