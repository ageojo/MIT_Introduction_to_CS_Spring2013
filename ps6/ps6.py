# Problem Set 6: Simulating robots
# Name: Amy C. Geojo
# scgreene@mit.edu


import math
import random

import ps6_visualize
import pylab

# For python 2.6:
#from ps6_verify_movement26 import testRobotMovement

# If you get a "Bad magic number" ImportError, comment out what's above and
# uncomment this line (for python 2.7):
from ps6_verify_movement27 import testRobotMovement

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.w = width
        self.h = height
        self.cleanTiles = {}
        for x in range(self.w):
            for y in range(self.h):
                self.cleanTiles[(x, y)] = False
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.cleanTiles[(math.floor(pos.getX()), math.floor(pos.getY()))] = True
       

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        
        return self.cleanTiles[(math.floor(m), math.floor(n))]

    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.w * self.h


    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """

        return sum(self.cleanTiles.values())
    

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        xRandom = random.random()*self.w
        yRandom = random.random()*self.h
        pos = Position(xRandom, yRandom)
        return pos
        


    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.getX() < self.w and pos.getX() >=0 and pos.getY() < self.h and pos.getY() >= 0



class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed     #float; given and constant throughout simulation; at each time-step, robot moves in its direction of motion by s units
        self.position = self.room.getRandomPosition()
        self.direction = random.randrange(0, 360)    #integer d, such that 0 <= d < 360; gives angle in degrees
 
        

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
    

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position


    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction


    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        curPos = self.getRobotPosition() # get robot's current position
        curDirection = self.getRobotDirection()

        newPos = curPos.getNewPosition(curDirection, self.speed) #getNewPosition (position argument) takes angle (direction) and speed arguments
        
        if self.room.isPositionInRoom(newPos):   #rectObject fx isPositionInRoom; takes position argument; returns T/F
            self.setRobotPosition(newPos)   #set pos as newPosition
            self.room.cleanTileAtPosition(newPos) #mark tile at that position as cleaned; note fx operates over RectObject which takes position argument
        else:
            self.direction = random.randrange(360)  #if new position isn't in room, at timestep robot selects new direction

        

# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """

    timeSteps = 0 #count # of time steps it takes to clean room given parameters

    
    for t in xrange(num_trials):
        allRobots = []
        room = RectangularRoom(width, height)   #put list generation and room within this for loop-- so they are re-freshed after each trial run
        for n in xrange(num_robots):
            robot = robot_type(room, speed)  #this looks at each individual robot cleaning rather than total robots
## Are the following 2 lines (setRobotPosition and setRobotDirection redundant?)
            robot.setRobotPosition(robot.room.getRandomPosition()) #get a random position that is in teh room 
            robot.setRobotDirection(random.randrange(0, 360))
            allRobots.append(robot)
            
        while float(room.getNumCleanedTiles())/room.getNumTiles() < min_coverage:
            for robot in allRobots:
                robot.updatePositionAndClean()
            timeSteps += 1

    return float(timeSteps)/num_trials    #this gives avg numSteps over number of trials of simulation            




# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """

    def __init__(self, room, speed):
        """
        creates an instance of RandomWalkRobot with the same attributes as Robot
        plus an additional attribute, step (used to track the number of
        updatePositionAndClean calls so RandomWalkRobot's behavior can differ on every other timeStep)
        """
        Robot.__init__(self, room, speed)
        self.step = 1


    
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        """
        select random direction after every other timestep (not just when hit wall)
        so, every other timestep, choosing location rather than moving
        """
        def pickMoveOrNewDir():
            if self.room.isPositionInRoom(newPos):   #RectangularObject fx isPositionInRoom; takes position argument; returns T/F
                    self.setRobotPosition(newPos)   #set pos as newPosition
                    self.room.cleanTileAtPosition(newPos) #mark tile at that position as cleaned; note fx operates over RectObject which takes position argument
            else:
                self.direction = random.randrange(360)                  

        self.step += 1   #increase value of step attribite on every call so robot behavior varies across even & odd trials (see mod below)
        curPos = self.getRobotPosition() # get robot's current position
        curDirection = self.getRobotDirection()
        newPos = curPos.getNewPosition(curDirection, self.speed)
        
        if self.step%2 == 0:  #on even time steps, only choose new dir if hit wall; on odd timesteps, choose new direction, & if not wall, move & clean; otherwise pick again
             pickMoveOrNewDir()

        else:
            self.direction = random.randrange(360)
            newPos = curPos.getNewPosition(curDirection, self.speed)
            pickMoveOrNewDir()



##implementation of RandomWalkRobot check:
#testRobotMovement(RandomWalkRobot, RectangularRoom, delay = 1)


# === Problem 5
#
# 1a) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#
"""
showPlot1('Time to clean 80% of 20x20 room as a function of the number of robots', 'Number of robots', 'Number of time steps')
"""
#
# 1b) How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#
""" At smaller numbers of robots, RandomWalkRobots take about double the amount of time to clean a room
as StandardRobots; this difference decreases as the number of robots increases.
Overall, cleaning time for both types of robots appear to decrease exponentially"""
#
#
# 2a) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
"""
showPlot2('The effect of room aspect ratio on cleaning time', 'Room aspect ratio', 'Number of time steps')
"""

# 2b) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, 50x6
#
"""Cleaning time for RandomWalkRobots is positively correlated with aspect ratio: clean time increases
steeply and linearly with room aspect ratio. in contrast, clean time for StandardRobots is nearly independent
of aspect ratio (relatively constant across all aspect ratios tested--just over 300 time steps) and substantively lower
than the clean time for RandomWalkRobots even at the lowest aspect ratios"""
#
#
#
#

def showPlot1(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#showPlot1('Time to clean 80% of 20x20 room, varying # of robots', 'Number of robots', 'Number of time steps')
    
def showPlot2(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

#showPlot2('The effect of room aspect ratio on cleaning time (simulated with 2 robots, 80% of room cleaned)', 'Room aspect ratio', 'Number of time steps')
