## Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
## Name: Amy Geojo


import numpy
import random
import pylab


#from ps7b_precompiled_27 import*


''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''


# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = float(maxBirthProb)
        self.clearProb = float(clearProb)
       

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        return random.random() <= self.clearProb      #floating pt # equality issue


    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        raise NoChildException
    

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses   #list rep virus pop. (SimpleVirus instances)
        self.maxPop = float(maxPop)


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)
       

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """             
        virusList = []

        for vir in self.viruses:
            if not vir.doesClear():
                virusList.append(vir)

        self.viruses = virusList                                
        popDensity = self.getTotalPop()/self.maxPop

        for vir in self.viruses:
            try:
                self.viruses.append(vir.reproduce(popDensity))
            except NoChildException:
                continue     #or should i just put except NoChildExcept  (w/ nothing else?)

        return self.getTotalPop()
           

# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTimeSteps, numTrials):
    """
    Runs the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for numTimeSteps timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    numTimeSteps: number of time steps per trial (an integer)
    numTrials: number of simulation runs to execute (an integer)
    """
##    virusList = []
##    for n in range(numViruses):
##        virusList.append(SimpleVirus(maxBirthProb, clearProb))
        
    virusList = [SimpleVirus(maxBirthProb, clearProb) for n in range(numViruses)]
    virusPopTime = {}
    virusPopTime[0] = numViruses*numTrials   #y-axis of avg # of viruses at eat timeStep ^actually, multiply by numTrials so when divide it is numTrials?
        
    for t in xrange(numTrials):
        patient = Patient(virusList, maxPop)
        for s in xrange(1, numTimeSteps + 1):
            try:
                virusPopTime[s] += patient.update()
                
            except KeyError:
                virusPopTime[s] = patient.update()

    for v in virusPopTime:
        virusPopTime[v] /= float(numTrials) 

    pylab.plot(virusPopTime.keys(), virusPopTime.values(), label = 'SimpleVirus')
    pylab.title('Simple Virus Simulation') #(no anti-virals, viruses are not drug-resistent)
    pylab.xlabel('Time Step')
    pylab.ylabel('Number of viruses')
    pylab.legend(loc = "best")
    pylab.savefig('Problem 4: SimpleVirus Simulation')
    pylab.show()
    

# PLOT Simulation 1: save graph and include 2 answers along with write-up; virus pop = 300; numTrials ~100
#simulationWithoutDrug(100, 1000, 0.1, 0.05, 300, 100)
#simulationWithoutDrug(100, 1000, 0.1, 0.05, 300, 1)

#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initializes a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: maximum reproduction probability (a float between 0-1)       

        clearProb: maximum clearance probability (a float between 0-1).

        resistances: a dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'fredonol':False, 'armandol':False}, means that this virus
        particle is resistant to neither fredonol nor armandol.

        mutProb: mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances.copy()     #resistances = {} with drug:T/F 
        self.mutProb = float(mutProb)

    def isResistantTo(self, drug):
        """
        Gets the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: the drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        try:
            return self.resistances[drug]
        except KeyError:
            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to fredonol but not
        armandol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to fredonol and a 90%
        chance that the offspring will be resistant to fredonol.
        There is also a 10% chance that the offspring will gain resistance to
        armandol and a 90% chance that the offspring will not be resistant to
        armandol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """        
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException
        
        if random.random() < self.maxBirthProb * (1- popDensity):
            ChildVir = ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
            for r in self.resistances:
                if random.random() < (1 - ChildVir.mutProb):
                    ChildVir.resistances[r] = self.resistances[r]
                else:
                    ChildVir.resistances[r] = not self.resistances[r]
              
            return ChildVir
        else:
            raise NoChildException
           

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.prescriptions = []   #empty list; intiially patient is drug-free


    def addPrescription(self, newDrug):
        """
        Administers a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)
            

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescriptions

    def getResistPop(self, drugResist):
        """
        Gets the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['fredonol'] or ['fredonol', 'armandol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        drugResistVirusPop = 0
        for virus in self.viruses:
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    break      #break out of this for loop if it is not resistant to one of the drugs; then check next virus; only add 1 to drugResistVirusPop list if virus is resistant to all the drugs in drugResist
                drugResistVirusPop +=1
        return drugResistVirusPop


    def update(self):
        """
        Updates the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """           
        virusList = []

        for vir in self.viruses:
            if not vir.doesClear():           #stochastically determine whether virus survives at time-step; not dependent upon drug resistance status of virus 
                virusList.append(vir)

        self.viruses = virusList                                
        popDensity = float(self.getTotalPop())/self.maxPop    #get popDensity of suriving viruses/max pop possible (includes surviving non-resistant viruses)

## reproduce function only considers viruses that are resistant to all drugs for reproduction 
        virusCopy = []
        for vir in self.viruses:
            try:
                virusCopy.append(vir.reproduce(popDensity, self.getPrescriptions()))
            except NoChildException:
                continue     #or should i just put except NoChildExcept  (w/ nothing else?)
        self.viruses.extend(virusCopy)    #add the baby viruses to the set of viruses already in patient

        return self.getTotalPop()     
           



#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTimeStepsNoDrugs, numTimeStepsWithDrugs, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds fredonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the fredonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'fredonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTimeStepsNoDrugs: number of time steps without drugs per trial (an integer)
    numTimeStepsWithDrugs: number of time steps with drugs per trial (an integer)
    numTrials: number of simulation runs to execute (an integer)
    
    """
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for n in range(numViruses)]
    totalVirusPop = {} #{0 : numViruses*numTrials}
    resistantVirusPop = {}

    for t in xrange(numTrials):
##        (totalVirusPop, resistantVirusPop) =  oneTrialSimulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
##                       mutProb, numTimeStepsNoDrugs, numTimeStepsWithDrugs)
##        
        patient = TreatedPatient(viruses, maxPop)
        for s in xrange(numTimeStepsNoDrugs + numTimeStepsWithDrugs):
            if s == numTimeStepsNoDrugs + 1:
                patient.addPrescription('fredonol')
            try:
                totalVirusPop[s] += patient.update()
                resistantVirusPop[s] += patient.getResistPop(['fredonol'])
            except KeyError:
                totalVirusPop[s] = patient.update()
                resistantVirusPop[s] = patient.getResistPop(['fredonol'])

    for v in totalVirusPop:
        totalVirusPop[v] /= float(numTrials)
        resistantVirusPop[v] /= float(numTrials)




        
    pylab.plot(totalVirusPop.keys(), totalVirusPop.values(), label = "Total # Viruses")
    pylab.plot(resistantVirusPop.keys(), resistantVirusPop.values(), label = "# of ResistantViruses")
    pylab.title('ResistantVirus Simulation')
    pylab.legend(loc = "best")
    pylab.xlabel('Time Period')
    pylab.ylabel('Number of Viruses')
    pylab.savefig('Problem 5: Simulation with Drug')
    pylab.show()

#simulationWithDrug(100, 1000, 0.1, 0.05, {'fredonol': False}, 0.005, 150, 150, 10)
#simulationWithDrug(100, 1000, 0.1, 0.05, {'fredonol': False}, 0.005, 150, 150, 100)
#simulationWithDrug(100, 1000, 0.1, 0.05, {'fredonol': False}, 0.005, 150, 150, 200)

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTimeStepsNoDrugs, numTimeStepsWithDrugs, numTrials):

    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for n in range(numViruses)]
    totalVirusPop = {} #{0 : numViruses*numTrials}
    resistantVirusPop = {}
    steps = numTimeStepsNoDrugs + numTimeStepsWithDrugs
    for t in xrange(numTrials):
        
        patient = TreatedPatient(viruses, maxPop)
        for s in xrange(steps):
            if s == numTimeStepsNoDrugs + 1:
                patient.addPrescription('fredonol')
            try:
                totalVirusPop[s] += patient.update()
                resistantVirusPop[s] += patient.getResistPop(['fredonol'])
            except KeyError:
                totalVirusPop[s] = patient.update()
                resistantVirusPop[s] = patient.getResistPop(['fredonol'])

    for v in totalVirusPop:
        totalVirusPop[v] /= float(numTrials)
        resistantVirusPop[v] /= float(numTrials)

    return (totalVirusPop.values(), resistantVirusPop.values())



# PROBLEM 6
#        
def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb,
                               resistances, mutProb, numTrials):
    """
    Runs simulations and make histograms for problem 6.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a list of drugs that each ResistantVirus is resistant to
                 (a list of strings, e.g., ['fredonol'])
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    """
    
    # TODO
    delay = [300, 150, 75, 0]

    for i in delay:
        numTimeStepsNoDrugs = i
        numTimeStepsWithDrugs = 150
        totalVirusPop, resistantVirusPop = simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                           mutProb, numTimeStepsNoDrugs, numTimeStepsWithDrugs, numTrials)
    

        pylab.hist(totalVirusPop, numTrials)
        pylab.title('Simulation with treatment delay:' + str(i))
        pylab.xlabel('# of Viruses')
        pylab.ylabel('# of Trials')
        pylab.legend(loc = "best")
        pylab.savefig('Number of steps without drug: ' + str(i) + "NumTrials: " + str(numTrials))
        pylab.show()



#simulationDelayedTreatment(100, 1000, 0.1, 0.05, {'fredonol': False}, 0.005, 100)


