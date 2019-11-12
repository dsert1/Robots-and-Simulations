# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Deniz Sert
# Collaborators (discussion): Branden Speitzer, Stephanie Pang, Michael from Office Hours
# Time: 3 hrs

import math
import random
import matplotlib
#matplotlib.use("TkAgg")

from ps3_visualize import *
import pylab

# === Provided class Position, do NOT change
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class iRoom(object):
    """
    A iRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        
        self.tiles = {}
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[(x,y)] = self.dirt_amount

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        tile_x = math.floor(pos.get_x())
        tile_y = math.floor(pos.get_y())
        if capacity > self.tiles[(tile_x, tile_y)]:
            self.tiles[(tile_x, tile_y)] = 0
        else:
            self.tiles[(tile_x, tile_y)] = self.tiles[(tile_x, tile_y)] - capacity
        

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        
        if self.tiles[(m,n)] == 0:
            return True 
        else:
            return False
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        clean_tiles = 0
        for tile in self.tiles:
            if self.tiles[tile] == 0:
                clean_tiles+=1
        return clean_tiles

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        tile_x = math.floor(pos.get_x())
        tile_y = math.floor(pos.get_y())
        if tile_x < 0 or tile_x>=self.width:
            return False
        if tile_y < 0 or tile_y>=self.height:
            return False
        
        return True

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.tiles[(m,n)]

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width*self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        x = random.random()*self.width
        y = random.random()*self.height
        return Position(x, y)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_pos_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a iRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot
                  in a single time-step
        """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        
        
#        x = random.random()*room.get_width()
#        y = random.random()*room.get_height()
        
        self.angle = random.random()*360.0
        self.position = room.get_random_position()
        

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.angle
    def get_robot_speed(self):
        return self.speed
    def get_room(self):
        return self.room
    def get_capacity(self):
        return self.capacity

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.angle = direction

    def update_pos_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Moves robot to new position and cleans tile according to robot movement
        rules.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class SimpleRobot(Robot):
    """
    A SimpleRobot is a Robot with the standard movement strategy.

    At each time-step, a SimpleRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_pos_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by capacity amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """
        #sets position
        position = self.position
        robot_direction = self.get_robot_direction()
        robot_speed = self.get_robot_speed()
        
        #finds a new position based on the previous position
        upgraded_pos = position.get_new_position(robot_direction, robot_speed)
        
        #checks to see if the new position is in room, if yes, cleans
        if self.get_room().is_position_in_room(upgraded_pos):
            self.set_robot_position(upgraded_pos)
            self.get_room().clean_tile_at_position(upgraded_pos, self.get_capacity())
        else: #if new position is not in room, turn
            self.set_robot_direction(random.random()*360.0)
        
        
        
        
       # self.set_robot_position()


# Uncomment this line to see your implementation of SimpleRobot in action!
#test_robot_movement(SimpleRobot, iRoom)

# === Problem 3
class OnSaleRobot(Robot):
    """
    A OnSaleRobot is a robot that may accidentally dirty a tile. A OnSaleRobot will
    drop some dirt on the tile it moves to and picks a new, random direction for itself
    with probability p = 0.05 rather than simply cleaning the tile it moves to. If the
    robot does drop dirt, the amount of dropped dirt should be an decimal value between 0 and 1.
    """
    p = 0.05

    @staticmethod
    def set_dirt_probability(prob):
        """
        Sets the probability of the robot accidentally dirtying the tile equal to prob.

        prob: a float (0 <= prob <= 1)
        """
        OnSaleRobot.p = prob

    def dropping_dirt(self):
        """
        Answers the question: Does the robot accidentally drop dirt on the tile
        at this timestep?
        The robot drops dirt with probability p.

        returns: True if the robot drops dirt on its tile, False otherwise.
        """
        return random.random() < OnSaleRobot.p

    def update_pos_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.
        If that position is valid, move the robot to that position. If it is not a valid position,
        the robot should change to a random direction.

        If the position is valid, check if the robot accidentally releases dirt. If so, dirty the new tile
        tile by a random decimal value between 0 and 1 and change its direction randomly.

        If the robot does not accidentally drop dirt, the robot should behave like
        SimpleRobot and clean the new position by capacity amount.
        """
        #sets position
        position = self.get_robot_position()
        robot_direction = self.get_robot_direction()
        robot_speed = self.get_robot_speed()
        
        #finds a new position based on the previous position
        upgraded_pos = position.get_new_position(robot_direction, robot_speed)
        
        #checks to see if the new position is in room, if yes, cleans
        if self.get_room().is_position_in_room(upgraded_pos):
            if self.dropping_dirt(): #robot could drop dirt
                self.get_room().clean_tile_at_position(upgraded_pos, random.random()*(-1))
                self.set_robot_direction(random.random()*360.0)
            else:
                self.set_robot_position(upgraded_pos)
                self.get_room().clean_tile_at_position(upgraded_pos, self.get_capacity())
        else: #if new position is not in room, turn
            self.set_robot_direction(random.random()*360.0)


#test_robot_movement(OnSaleRobot, iRoom)


# === Problem 4
class BreathtakingRobot(Robot):
    """
    A BreathtakingRobot is a robot that moves extra fast and can clean two tiles in one
    timestep.

    It moves in its current direction, cleans the tile it lands on, and continues
    moving in that direction and cleans the second tile it lands on, all in one
    unit of time.

    If the BreathtakingRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can
    knock dust off of the wall.

    """
    p = 0.15

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        BreathtakingRobot.p = prob

    def dropping_dirt(self):
        """
        Answers the question: Does the robot accidentally drop dirt on the tile
        at this timestep?
        The robot drops dirt with probability p.

        returns: True if the robot drops dirt on its tile, False otherwise.
        """
        return random.random() < BreathtakingRobot.p

    def update_pos_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Within one time step (i.e. one call to update_pos_and_clean), there are
        three possible cases:

        1. The next position in the current direction at the robot's given speed is
           not a valid position in the room, so the robot stays at its current position
           without cleaning the tile. The robot then turns to a random direction.

        2. The robot successfully moves forward one position in the current direction
           at its given speed. Let's call this Position A. The robot cleans Position A.
           The next position in the current direction is not a valid position in the
           room, so it does not move to the new location. With probability p, it dirties
           Position A by 1. Regardless of whether or not the robot dirties Position A,
           the robot will turn to a random direction.

        3. The robot successfully moves forward two positions in the current direction
           at its given speed. It cleans each position that it lands on.
        """
        #sets position
        position = self.get_robot_position()
        robot_direction = self.get_robot_direction()
        robot_speed = self.get_robot_speed()
        
        upgraded_pos = position.get_new_position(robot_direction, robot_speed)
        
        
        
        if not self.get_room().is_position_in_room(upgraded_pos): #position is not in room
            self.set_robot_direction(random.random()*360.0)
        #moves 1 step and could dirty the position 
        else:
            self.set_robot_position(upgraded_pos)
            self.get_room().clean_tile_at_position(upgraded_pos, self.get_capacity())
            
            #checks to see if new position is in room
            pos_B = upgraded_pos.get_new_position(robot_direction, robot_speed)
            if self.get_room().is_position_in_room(pos_B):
                self.set_robot_position(pos_B)
                self.get_room().clean_tile_at_position(pos_B, self.get_capacity())
             
            else:
                #could drop dirt
                if self.dropping_dirt():
                    self.get_room().clean_tile_at_position(upgraded_pos, (-1))
                self.set_robot_direction(random.random()*360.0)
                
        


#if self.dropping_dirt():
#                self.get_room().clean_tile_at_position(upgraded_pos, random.random()*(-1))
#                self.set_robot_direction(random.random()*360.0)
#test_robot_movement(BreathtakingRobot, iRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile. Each trial is run in its own iRoom
    with its own robots.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. SimpleRobot or
                OnSaleRobot)
    """
    #for loop through trials
    #use docstring to run -> straightforward
    total_count = 0 #trials
    
    for i in range(num_trials):
        inner_count = 0
        robots = []
        room = iRoom(width, height, dirt_amount)
        for i in range(num_robots):
            robots.append(robot_type(room, speed, capacity))
        coverage= room.get_num_cleaned_tiles()/room.get_num_tiles()
            
        while coverage<min_coverage:
            for robot in robots:
                robot.update_pos_and_clean()
            inner_count+=1
            coverage= room.get_num_cleaned_tiles()/room.get_num_tiles()
            
        total_count+=inner_count        
        
    return total_count/num_trials

#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, SimpleRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, SimpleRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, SimpleRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, SimpleRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, SimpleRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
#
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SimpleRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, OnSaleRobot))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, BreathtakingRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('SimpleRobot', 'OnSaleRobot', 'BreathtakingRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SimpleRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, OnSaleRobot))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, BreathtakingRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('SimpleRobot', 'OnSaleRobot', 'BreathtakingRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time (steps)')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time (steps)')