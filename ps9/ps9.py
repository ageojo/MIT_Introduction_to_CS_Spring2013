# 6.00 Problem Set 9 Spring 2013
#
# Name: Amy Geojo


import pylab
import random
import time
import collections

'''
Begin helper code
'''
def printSubjects(subjects, sortOutput=True):
    """
    Pretty-prints a list of Subject instances using the __str__ method
    of the Subject class.

    Parameters:
    subjects: a list of Subject instances to be printed
    sortOutput: boolean that indicates whether the output should be sorted
    according to the lexicographic order of the subject names
    """
    if sortOutput:
        subjectCmp = lambda s1, s2: cmp(s1.getName(), s2.getName())
        sortedSubjects = sorted(subjects, cmp=subjectCmp)
    else:
        sortedSubjects = subjects
        
    print 'Course\tValue\tWork\tLottery\n======\t=====\t====\t===='
    totalValue, totalWork, numLotteried = 0, 0, 0
    for subject in sortedSubjects:
        print subject
        totalValue += subject.getValue()
        totalWork += subject.getWork()
        numLotteried += subject.getLottery()

    print '\nNumber of subjects: %d\nTotal value: %d\nTotal work: %d \nTotal number of lottery subjects: %i \n' % \
          (len(subjects), totalValue, totalWork, numLotteried)
'''
End Helper Code
'''
##############
## Problem 1
##############
class Subject(object):
    """
    A class that represents a subject.
    """
    def __init__(self, name, value, work, lottery):
        """
        Initializes a Subject instance.

        Parameters:
        name: a string that represents the name of the subject
        value: an integer that represents the value for the subject
        work: an integer that represents the amount of work for the subject
        lottery: a binary integer represents if this subject is lottery based
        """
        self.name = name
        self.value = value
        self.work = work
        self.lottery = lottery
        
    def getName(self):
        """
        Gets the name of the subject.

        Returns: a string that represents the name of the subject
        """
        return self.name
    
    def getValue(self):
        """
        Gets the value of the subject.
        
        Returns: an integer that represents the value of the subject
        """
        return self.value

    def getWork(self):
        """
        Gets the amount of work for the subject.

        Returns: an integer that represents the work amount of the subject
        """
        return self.work

    def getLottery(self):
        """
        Gets 1 if the subject is a lottery or 0 otherwise.

        Returns: a binary integer that represents if the subject is a lottery
        """
        return self.lottery


    def __str__(self):
        """
        Generates the string representation of the Subject class.

        Returns:
        a string of the form <subject name>\t<value>\t<work>\t<lottery>
        where \t is the tab character
        """
        return str(self.getName()) + '\t' + str(self.getValue()) + '\t' + str(self.getWork()) + '\t' + str(self.getLottery())

    
###############
## PROBLEM 1
###############
def loadSubjects(filename):
    """
    Loads in the subjects contained in the given file. Assumes each line of
    the file
    is of the form "<subject name>,<value>,<work>,<lottery>" where
    each field is separated by a comma. Whether a subject is lotteried is represented with 1 meaning that subject
    is lotteried, 0 meaning it is not.

    Parameter:
    filename: name of the data file as a string

    Returns:
    a list of Subject instances, each representing one line from the data file
    """
    subjectList = []
    subjects = open(filename, 'r')
    for line in subjects:
        field = line.strip().split(',')
        name = field[0]
        value = float(field[1])
        work = float(field[2])
        lottery = float(field[3])
        subjectList.append(Subject(name, value, work, lottery))
    subjects.close()
    return subjectList


class SubjectAdvisor(object):
    """
    An abstract class that represents all subject advisors.
    """
    
    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Pick a set of subjects from the subjects list such that the value of
        the picked set is maximized, with the constraint that the total amount
        of work of the picked set needs to be <= maxWork and the total mount of
        lotteries subjects is <=maxLottery. To be implemented by subclasses.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lottery subjects student is allowed to take.

        Returns:
        a list of Subject instances that are chosen to take
        """

        raise NotImplementedError('Should not call SubjectAdvisor.pickSubjects!')

    def getName(self):
        """
        Gets the name of the advisor. Useful for generating plot legends. To be
        implemented by subclasses.

        Returns:
        A string that represents the name of this advisor
        """
        raise NotImplementedError('Should not call SubjectAdvisor.getName!')


###############
## PROBLEM 2
###############
def cmpValue(subject1, subject2):
    """
    A comparator function for two subjects based on their values. To be used
    by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has more value than subject2, 1 if subject1 has less value
    than subject2, 0 otherwise
    """
    return cmp(subject2.getValue(), subject1.getValue())    #if sub1 more, -1; y > x
#cmp(x,y); if x<y, returns negative; x == y returns 0; x > y, returns positive


def cmpWork(subject1, subject2):
    """
    A comparator function for two subjects based on their amount of work.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has less work than subject2, 1 if subject1 has more work
    than subject2, 0 otherwise
    """

    return cmp(subject1.getWork(), subject2.getWork()) #if sub1 less work, -1 (x<y)
  

def cmpRatio(subject1, subject2):
    """
    A comparator function for two subjects based on their value to work ratio.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has higher value to work ratio than subject2, 1 if subject1
    has lower value to work ratio than subject1, 0 otherwise
    """
    return cmp(subject2.getValue()/subject2.getWork(), subject1.getValue()/subject1.getWork())
   # x > y, 1; sub1 > sub2, -1, hence reversed order

###########################
## PROBLEM 2 (continued)
###########################
class GreedyAdvisor(SubjectAdvisor):
    """
    An advisor that picks subjects based on a greedy algorithm.
    """
    
    def __init__(self, comparator):
        """
        Initializes a GreedyAdvisor instance.

        Parameter:
        comparator: a comparator function, either one of cmpValue, cmpWork,
                    or cmpRatio
        """
        self.comparator = comparator

    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Picks subjects to take from the subjects list using a greedy algorithm,
        based on the comparator function that is passed in during
        initialization.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lotteried subjects a student can take

        Returns:
        a list of Subject instances that are chosen to take
        """
        courseList = []
        workCount = 0.0
        lotteryCount = 0.0

        for sub in sorted(subjects, cmp = self.comparator, reverse = True): #does cmp work this way?    ##think merge sort for how cmp is working w 2 arg
            wk = sub.getWork()
            lot = sub.getLottery()
            if wk + workCount <= maxWork and lot + lotteryCount <= maxLottery:
                courseList.append(sub)
                workCount += wk
                lotteryCount += lot
        return courseList

    def getName(self):
        """
        Gets the name of the advisor. 

        Returns:
        A string that represents the name of this advisor
        """
        return "Greedy"


##############
## PROBLEM 3
##############
class BruteForceAdvisor(SubjectAdvisor):

    def __init__(self):
        """
        Initializes a BruteForceAdvisor instance.
        """
        pass

    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Pick subjects to take using brute force. Use recursive backtracking
        while exploring the list of subjects in order to cut down the number
        of paths to explore, rather than exhaustive enumeration
        that evaluates every possible list of subjects from the power set.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lottery subjects student is allowed to take.

        Returns:
        a list of Subject instances that are chosen to take
        """
        if subjects == [] or maxWork == 0:
            result = []
        elif subjects[0].getWork() > maxWork or subjects[0].getLottery() > maxLottery:
            result = self.pickSubjects(subjects[1:], maxWork, maxLottery)
        else:
            nextItem = subjects[0]

            # solve subproblem WITH next item & reduced maxWork and maxLottery
            withToTake = self.pickSubjects(subjects[1:], maxWork - nextItem.getWork(), maxLottery - nextItem.getLottery())
            withVal = nextItem.getValue() + sum([subject.getValue() for subject in withToTake])

            #solve subproblem WITHOUT nextItem & reduced maxWork and maxLottery
            withoutToTake = self.pickSubjects(subjects[1:], maxWork, maxLottery)
            withoutVal = sum([subject.getValue() for subject in withoutToTake])

            if withVal > withoutVal:
                result = [nextItem] + withToTake
            else:
               result = withoutToTake               
        return result
    

    def getName(self):
        """
        Gets the name of the advisor. 

        Returns:
        A string that represents the name of this advisor
        """
        return "Brute Force"

##############
## PROBLEM 4
##############

def stringNames(subjects):
    string = ''
    for sub in subjects:
        string += sub.getName()
    return string


class MemoizingAdvisor(SubjectAdvisor):

    def __init__(self):
        """
        Initializes a MemoizingAdvisor instance.
        """
        self.memo = {}


    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Pick subjects to take using memoization. Similar to
        BruteForceAdvisor except that the intermediate results are
        saved in order to avoid re-computation of previously traversed
        subject lists.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lottery subjects student is allowed to take.

        Returns:
        a list of Subject instances that are chosen to take
        """
        names = stringNames(subjects)

        if (names, maxWork, maxLottery) in self.memo:
            return self.memo[names, maxWork, maxLottery]

        if subjects == [] or maxWork == 0:
            result = []
            
        elif subjects[0].getWork() > maxWork or subjects[0].getLottery() > maxLottery:
            result = self.pickSubjects(subjects[1:], maxWork, maxLottery)
        else:
            nextItem = subjects[0]

            # solve subproblem WITH next item & reduced maxWork and maxLottery
            withToTake = self.pickSubjects(subjects[1:], maxWork - nextItem.getWork(), maxLottery - nextItem.getLottery())
            withVal = nextItem.getValue() + sum([subject.getValue() for subject in withToTake])
            
            #solve subproblem WITHOUT nextItem & reduced maxWork and maxLottery
            withoutToTake = self.pickSubjects(subjects[1:], maxWork, maxLottery)
            withoutVal = sum([subject.getValue() for subject in withoutToTake])
                       
            if withVal > withoutVal:
                result = ([nextItem] + withToTake)                                             
            else:
               result = (withoutToTake)
                                              
        self.memo[(names, maxWork, maxLottery)]  = result
        return result
    
#memo maps to value of subjects; need to include all relevant -- name, max work, max lot  = value; but remember, need to return list of subjects
          #want to return list of subject instances
       

    def getName(self):
        """
        Gets the name of the advisor.

        Returns:
        A string that represents the name of this advisor
        """
        return "Memoizing"
    
##############
## PROBLEM 5
##############
def measureTimes(filename, maxWork, maxLottery, subjectSizes, numRuns):
    """
    Compare the time taken to pick subjects for each of the advisors
    subject to maxWork constraint. Run different trials using different number
    of subjects as given in subjectSizes, using the subjects as loaded
    from filename. Choose a random subject of subjects for each trial.
    For instance, if subjectSizes is the list [10, 20, 30], then you should
    first select 10 random subjects from the loaded subjects, then run them
    through the three advisors using maxWork and maxLottery for numRuns times,
    measuring the time taken for each run, then average over the numRuns runs. After that,
    pick another set of 20 random subjects from the loaded subjects,
    and run them through the advisors, etc. Produce a plot afterwards
    with the x-axis showing number of subjects used, and y-axis showing
    time. Be sure you label your plots.

    After plotting the results, answer this question:
    What trend do you observe among the three advisors?
    How does the time taken to pick subjects grow as the number of subject
    used increases? Why do you think that is the case? Include the answers
    to these questions in your writeup.
    """
    
    def runTrial(subjects, maxWork, maxLottery, subjectSizes, advisor):
        """
        len(subjectSizes) # of runs with each run containing subjectSizes number of randomly chosen
        subjects from list of subjects; then for particular advisor selected, and maxWork and maxLottery
        constraints, computes the subjects selected and the runtime for a given computation
        Returns a tuple containing 2 lists: advisedSubjects is a list of subjects. totalTime is a list of runTimes
        """        
        result = {}
        for num in subjectSizes:
            selected = random.sample(subjects, num)  #for each subj size, select that # of subjects from list of subjects
            start = time.time()
            advisor.pickSubjects(selected, maxWork, maxLottery) #run to get selected subjects and add to list;
            end = time.time()
            totalTime = end - start
            result[num] = round(totalTime, 4)
        return result
            

    def addDict(d1, d2):
        """
        d1 and d2 are two dictionaries.
        Returns a dictionary that adds the
        values of keys that are in d1 and d2
        """
        d3 = {}
        for key in d1.keys():
            d3[key] = 0
        for i in d1:
            if i in d2.keys():
                d3[i] = d1[i] + d2[i]       
        return d3

    def addDictList(dlist):
        """
        dlist is a list of dictionaries
        Returns a dictionary that adds the values of keys
        in each dictionary in dlist
        """
        x = {}
        for d in dlist:
            x = addDict(d, x)
        return x


##    def plot(d, title, xlabel, ylabel):
##        """
##        takes a dictionary, d, and three strings for the title
##        of the graph and x-axis and y-axis labels;
##        Returns a plot with keys as x-values and the values as
##        y-values
##        """
##        pylab.plot(d.keys(), d.values())
##        pylab.title(title)
##        pylab.xlabel(xlabel)
##        pylab.ylabel(ylabel)
##        pylab.legend(loc = "best")
##        pylab.savefig(title)
##        pylab.show()

##########################################
    ## End helper functions ##
        
    StartTime = time.time()
    
    subjects = loadSubjects(filename)    
    
    Greedy = GreedyAdvisor(cmpRatio)
    BruteForce = BruteForceAdvisor()
    Memoizing = MemoizingAdvisor()
    
    greedy = []
    brute = []
    memoize = []

    random.shuffle(subjectSizes)
    
    for i in xrange(numRuns):
        greedy.append(runTrial(subjects, maxWork, maxLottery, subjectSizes, Greedy))
        brute.append((runTrial(subjects, maxWork, maxLottery, subjectSizes, BruteForce)))
        memoize.append(runTrial(subjects, maxWork, maxLottery, subjectSizes, Memoizing))
    
    
    greedy = addDictList(greedy)
    brute = addDictList(brute)
    memoize = addDictList(memoize)
    
    for key in sorted(subjectSizes):
        greedy[key]/= numRuns
        brute[key]/= numRuns
        memoize[key]/= numRuns

    greedy = collections.OrderedDict(sorted(greedy.items()))
    brute = collections.OrderedDict(sorted(brute.items()))
    memoize = collections.OrderedDict(sorted(memoize.items()))

    print "greedy: " + str(greedy)
    print "brute: " + str(brute)
    print "memoize: " + str(memoize)

    EndTime = time.time()
    print "Total run-time is: " + str(EndTime - StartTime)

#produce plots comparing run-times for different numbers of subjects chosen, constraints: maxWork & maxLottery
    pylab.plot(greedy.keys(), greedy.values(), label = 'Greedy')
    pylab.plot(brute.keys(), brute.values(), label = 'BruteForce')
    pylab.plot(memoize.keys(), memoize.values(), label = 'Memoize')
    pylab.semilogy()
    pylab.title('Comparing Greedy, Brute and Memoize advisors')
    pylab.xlabel('# of subjects')
    pylab.ylabel('Run-time (sec)')  # + '/n' + 'totalTime = ' + str(EndTime - StartTime))
    pylab.legend(loc = "best")
    pylab.savefig('pset9__Greedy_Brute_Memoize_Advisors')
    pylab.show()
                    
##    plot(greedy, "Greedy Advisor", "# of subjects selected", "Run-time")
##    plot(brute, "Brute Force Advisor", "# of subjects selected", "Run-time")
##    plot(memoize, "Memoizing Advisor", "# of subjects selected", "Run-time")
##    pylab.show()


if __name__ == "__main__":
    """
    Using data from subjects.txt and subjects_small.txt, compare different algorithms
    for choosing optimal set of courses for student
    """

    
    #measureTimes(filename, maxWork, maxLottery, subjectSizes, numRuns)
 #   measureTimes("subjects.txt", 40, 10, [10, 20, 30, 40, 50], 5)
 #   measureTimes("subjects.txt", 30, 5, [30, 50], 5)



##greedy: OrderedDict([(10, 8e-05), (20, 0.0001), (30, 0.00017999999999999998), (40, 0.00026), (50, 0.00033999999999999997)])
##brute: OrderedDict([(10, 0.0015800000000000002), (20, 0.05329999999999999), (30, 0.53772), (40, 6.87312), (50, 4.5812800000000005)])
##memoize: OrderedDict([(10, 0.00242), (20, 0.018439999999999998), (30, 0.0382), (40, 0.08154), (50, 0.10174000000000001)])
##Total run-time is: 149.090400934


    
##    subjects = loadSubjects("subjects_small.txt")
## #   printSubjects(subjects)
##    Greedy = GreedyAdvisor(cmpValue) 
##    printSubjects(Greedy.pickSubjects(subjects, 10, 2))
##
##    Brute = BruteForceAdvisor()
##    printSubjects(Brute.pickSubjects(subjects, 10, 2))
##
##    Memoizing = MemoizingAdvisor()
##    printSubjects(Memoizing.pickSubjects(subjects, 10, 2))



#    measureTimes("subjects.txt", 10, 3, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 20)          
##greedy: OrderedDict([(10, 5e-06), (20, 9.500000000000003e-05), (30, 0.000125), (40, 0.00020000000000000004), (50, 0.00028999999999999995), (60, 0.0003850000000000001), (70, 0.0004100000000000001), (80, 0.0004900000000000002), (90, 0.0005749999999999999), (100, 0.0006549999999999998)])
##brute: OrderedDict([(10, 0.00019499999999999997), (20, 0.0013200000000000004), (30, 0.005764999999999999), (40, 0.018555), (50, 0.04229), (60, 0.13146999999999998), (70, 0.5138149999999999), (80, 1.0904500000000001), (90, 1.28575), (100, 2.8420099999999993)])
##memoize: OrderedDict([(10, 0.00057), (20, 0.00626), (30, 0.005734999999999999), (40, 0.012625), (50, 0.020590000000000004), (60, 0.033105), (70, 0.047125), (80, 0.073215), (90, 0.08414999999999997), (100, 0.11208999999999998)])
##>>> 

