# Problem Set 10 - Clustering Songs
# Name: Amy Geojo


#Code shared across examples
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pylab, random, string, copy, math, csv
from cluster import *
from cvisualization import *

# Songs example
def readSongData(filename):
    '''
    Reads in song data, with 13 feature vectors, from
    filename
    '''
    name_list = []
    data_list=[]
    max_vals = []
    with open(filename, 'r') as data_file:
        reader = csv.reader(data_file)
        first = True
        for row in reader:
            # Skip the first line
            if first:
                first = False
                continue

            # Name is concatenation of artist_name:song_title
            name = row[0] + ':'+ row[2]
            # Rest is values
            data = pylab.array([float(val) for val in row[3:]])
            name_list.append(name)
            data_list.append(data)

        # Get the max values for each feature to normalize data
        for i in xrange(len(data_list[0])):
            max_vals.append(max(data[i] for data in data_list))

    return (name_list, data_list, pylab.array(max_vals))

def buildSongPoints(filename):
    '''
    Given an input filename, reads Song values form the file and returns
    them all in a list.
    '''
    name_list, data_list, max_vals = readSongData(filename)
    points = []
    for i in xrange(len(name_list)):
        originalAttrs = data_list[i]
        normalizedAttrs = originalAttrs/max_vals   #AG: why is this not max_vals[i] since this is a list of "artist_familiarity" 
        ###### BUILD THE ACTUAL SONGS WITH NORMALIZED ATTRIBUTES #######
        song = Song(name_list[i], originalAttrs, normalizedAttrs)
        points.append(song)
    return points

def getAveSongHotness(cluster):
    """
    Given a Cluster object, finds the average song hotness field over the members
    of that cluster.
    
    cluster: the Cluster object to check
    
    Returns: a float representing the computed average song hotness value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttr(Song.SongHotness)

    return float(tot) / len(cluster.getPoints())

def test(points, k = 200, cutoff = 0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    hotnesses = []
    print ''
    clusters, maxSmallest = kmeans(points, k, cutoff, Song)
    print(len(clusters))

    for clustNum in range(k):
        if len(clusters[clustNum].points) == 0:
            continue
        hotnesses.append(getAveSongHotness(clusters[clustNum]))

    pylab.hist(hotnesses)
    pylab.xlabel('Ave. Song Hotness')
    pylab.ylabel('Number of Clusters')
    pylab.show()
            
# Problem 1: Implement k-means in cluster.py
# Run the test function on the testPoints.

### points contains the _entire_ dataset
##points = buildSongPoints('songs.csv')
##
###testPoints contains but a tenth of them.
##testPoints = random.sample(points, len(points)/10)
##
##test(testPoints)



# Problem 2: Visualizing k-means

def visualizeClusters():
    '''
    Zeros out all but two of the dimensions in the Song feature
    vector.

    Then, makes an appropriate call to visual_kmeans using the Song
    testPoints dataset.
    
    Takes no parameters (necessary for the animation to work)
    '''    
    points = buildSongPoints('songs.csv')
    testPoints = random.sample(points, len(points)/10)

    for Song in testPoints:
        Song.equal_weights(0.0)
        Song.set_weight(Song.getAttr(1), 1.0) #1 is ArtistHotness
        Song.set_weight(Song.getAttr(9), 1.0)  # 9 is SongHotness

    ArtistHotness = [Song.getAttr(1) for Song in testPoints]
    SongHotness = [Song.getAttr(9) for Song in testPoints]
    
    visual_kmeans(figure, subplot, testPoints, 6, Song, ArtistHotness, SongHotness,\
                  delay=1, cutoff=0.1, minIters = 3, maxIters = 100)
    





    


# ******** Animation Code *************
## Uncomment the following 4 lines when you've defined visualizeClusters:
##figure = plt.figure()
##subplot = figure.add_subplot(111)
##figure.canvas.manager.window.after(100, visualizeClusters)
##plt.show()

# Problem 3: k-means and Individual Songs

def findSongCluster(points, song, k, cutoff = 0.1):
    '''
    Runs k-means clustering over points 3 times with the given k 
    and cutoff values. Each time the clustering is run, this function
    prints out the cluster that contains the specified song.

    points: a list of Point objects
    county: a string, the song we wish to examine
    k: int, the number of clusters we wish to use
    cutoff: float     
    '''
    for i in range(3):
        clusters, maxDist = kmeans(points, k, cutoff, Song)
        for c in clusters:
            if c.contains(song):
                print c


## testing fx above        
##points = buildSongPoints('songs.csv')
##testPoints = random.sample(points, len(points)/10)
##findSongCluster(points, "Kanye West / Lupe Fiasco: Touch The Sky (Amended Album Version)", k=55)
##findSongCluster(points, "Led Zeppelin: Immigrant Song (Album Version)", k=55)
##    
# Problem 4: Predicting Song Hotness with k-means

def CV(measured):
    """
    computes the coefficient of variance.
    """
    mean = measured.sum()/float(len(measured))
    sd = math.sqrt((((mean-measured)**2).sum()))
    return mean/sd


def graphPredictionErr(points, kvals, cutoff = 0.1):
    """    
    Given input points and a list of kvals, should cluster on the
    appropriate weight vectors and graph the error in the resulting
    predictions, as described in Problem 4.

    points: a list of Point objects
    kvals: a list of k values (integers)
    cutoff: float     
    """
    for p in points:
        p.equal_weights(0.0)
        p.set_weight(p.ArtistFamiliarilty, 1.0)
        p.set_weight(p.ArtistHotness, 1.0)
        p.set_weight(p.Year, 1.0)

    bestCV = []
    for k in kvals:
         clustersBest, maxDistBest = kmeans(points, k, cutoff, Song)
         #avgBestClusters[i].append(clustersBest)
         HotnessBestClusters = [getAveSongHotness(cluster) for cluster in clustersBest]
         CVEachCluster = [CV(i) for i in HotnessBestClusters]
         bestCV[k].append(CVEachCluster)

    for k in bestCV:
        CVbest = CV(k)
         
     
    for p in points:
        p.equal_weights(0.0)
        p.set_weight(p.Duration, 1.0)
        p.set_weight(p.FadeOutStart, 1.0)
        p.set_weight(p.SampleRate, 1.0)


    for k in kvals:
        clustersWorst, maxDistWorst = kmeans(points, k, cutoff, Song)
        HotnessWorstClusters = [getAveSongHotness(cluster) for cluster in clustersWorst]
        CVEachCluster = [CV(i) for i in HotnessWorstClusters]
        worstCV[k].append(CVEachCluster)

    for k in worstCV:
        CVworst = CV(k)


    pylab.plot(k, CVbest, label = "Best Predictors")
    pylab.plot(k, CVworst, label = "Worst Predictors")
    pylab.title("Predicting SongHotness")
    pylab.legend(loc = "best")
    pylab.savefig("Problem 4: Predicting SongHotness")
    pylab.show()



##points = buildSongPoints('songs.csv')
##kvals = [5, 15, 25, 35, 45, 55, 65, 75]
##graphPredictionErr(points, kvals, cutoff = 0.1)






### predicted to be highly correlated with song hotness
##ArtistFamiliarilty 0
##ArtistHotness 1
##Year 12
##
### predicted to not be very predictive of SongHotness
##Duration 4
##FadeOutStart 6
##SampleRate 8
 
