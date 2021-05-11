import random
import math
from tqdm import trange
import sys
import probability

#================================================================

WORLD = 200                                                                                         # 0.2 sq. km. scaled down from 200 sq. km.
population = 500                                                                                    # 500 people scaled down from 0.5 million.
initialInfected = round(population * 0.75 / 100)                                                    # Starting infected value.
InfectionDist = 3                                                                                   # 3 m. radius of infection.
spotInfectionDist = 1
MAX_Moves = 3                                                                                       # Individuals vist a max of 3 locations/day
Days = 100

MaskStatus = bool(int(input("Mask: ")))
GloveStatus = bool(int(input("Glove: ")))
LockdownStatus = bool(int(input("Lockdown: ")))


#================================================================================================================================================

class Human:

    # ID, Total Infected, Susceptible, Active Infections, Recovered, Deaths.
    counter = [0, 0, 0, 0, 0, 0]

    #================================================================

    # ID builder.
    def buildID(self):
        self.counter[0] += 1
        return self.counter[0]

    #================================================================

    def IncreaseInfections(self):
        self.counter[1] += 1                                                                        # Increae Total Infections.
        self.counter[3] += 1                                                                        # Increase Active Infections.

        if self.IC == True or probability.asymptomatic(self.age) == False:
            self.distanceCurrent = probability.distanceAfter(self.age, self.IC, WORLD, lockdown = LockdownStatus)                  # Set distance to AVG after.
            self.death = probability.death(self.age, self.IC)                                           # Find out if a death case.
        
        self.transition = probability.time(self.age, self.IC, self.death)                           # Find out recovery time.
        self.status = 5                                                                             # Set status to "Infected".

        self.spotX = [self.x]                                                                       # Add first spot-x position
        self.spotY = [self.y]                                                                       # Add first spot-y position
        self.spotRecTime = [2]                                                                      # Spots disappear after 2 movements.
    
    #================================================================

    def DecreaseInfections(self, D_R = 1):                                                          # D_R is Dead(0) or Recovered(1)
        self.counter[3] -= 1

        # Resetting spot values.
        self.spotX = None                                                                           
        self.spotY = None
        self.spotRecTime = None

        if D_R == 1:                                                                                # If Recovery patient:
            self.counter[4] += 1                                                                    # Increase recovered cases.
            self.distanceCurrent = self.distanceBefore                                              # Set distance to AVG Before.
            self.status = 0                                                                         # Set status to "Recovered",


        elif D_R == 0:                                                                              # If Death patient:
            self.counter[5] += 1                                                                    # Increase death cases.
            self.distanceCurrent = 0                                                                # Set distance to 0.
            self.status = -1                                                                        # Set status to "Dead".
    
    #================================================================

    def updateSusceptible(self):
        self.counter[2] = population - self.counter[1]

    #================================================================

    def __init__(self, X = None, Y = None):
        
        # ID builder.
        self.ID = self.buildID()

        # Assigning (x,y) positions for the first time.
        if X is None:
            X = random.randint(0, WORLD)
        if Y is None:
            Y = random.randint(0, WORLD)
        
        self.x = X
        self.y = Y

        self.prevx = X
        self.prevy = Y

        # Storing initial positions as homes of people.
        self.homeX = X
        self.homeY = Y

        # Spots for indirect infections.
        self.spotX = None
        self.spotY = None
        self.spotRecTime = None

        # Charactersitics.
        self.age = probability.age()
        self.IC = probability.IC(self.age)
        self.death = False
        self.transition = 0

        # Average maximum distance.
        self.distanceBefore = probability.distanceBefore(self.age, WORLD, lockdown = LockdownStatus)
        self.distanceCurrent = self.distanceBefore
        self.movementNumber = probability.movement(self.age, self.IC, lockdown = LockdownStatus)

        # Status integers:
        # 2: Susceptible, 5: Infected, 0: Recovered, -1: Dead.
        self.status = 2
    
    #================================================================

    def moveSimulation(self):                                                                       # Day comprising movements.

        self.prevx = self.x
        self.prevy = self.y

        tempX = self.x + random.randint(-self.distanceCurrent, self.distanceCurrent)
        if tempX < 0:
            tempX = 0
        elif tempX > WORLD:
            tempX = WORLD
        
        self.x = tempX
    
        tempY = self.y + random.randint(-self.distanceCurrent, self.distanceCurrent)
        if tempY < 0:
            tempY = 0
        elif tempY > WORLD:
            tempY = WORLD
        
        self.y = tempY

        # Spot changes.
        if self.status == 5:     

            for s in self.spotRecTime:                                                              # Decrease spot rec after every move.
                s -= 1

            for s in range(len(self.spotRecTime)):                                                  # Remove expired spots
                if self.spotRecTime[s] == 0:
                    self.spotRecTime.pop(s)
                    self.spotX.pop(s)
                    self.spotY.pop(s)
            
            # Add new spot.
            self.spotX.append(self.x)
            self.spotY.append(self.y)
            self.spotRecTime.append(2)

    #================================================================

    def moveHome(self):                                                                             # End of the day travel.
        
        self.prevx = self.x
        self.prevy = self.y

        self.x = self.homeX
        self.y = self.homeY

        if self.status == 5:                                                                        # If Infected:
            self.transition -= 1                                                                    # Reduce recovery days.
            if self.transition == 0:                                                                # If recovery period is over:
                if self.death == True:                                                              # Decrease infections according to case.
                    self.DecreaseInfections(0)                                        
                else:
                    self.DecreaseInfections(1)
        
        # Spot changes.
        if self.status == 5:     

            for s in self.spotRecTime:                                                              # Decrease spot rec after every move.
                s -= 1

            for s in range(len(self.spotRecTime)):                                                  # Remove expired spots
                if self.spotRecTime[s] == 0:
                    self.spotRecTime.pop(s)
                    self.spotX.pop(s)
                    self.spotY.pop(s)
            
            # Add new spot.
            self.spotX.append(self.x)
            self.spotY.append(self.y)
            self.spotRecTime.append(2)
    
    #================================================================

    def infect(self):

        if self.status == 2:
            self.IncreaseInfections()
    
    #================================================================

    def statusRec(self):

        statusDict = {"2":"Susceptible", "5":"Infected", "0":"Recovered", "-1":"Dead"}
        return statusDict[str(self.status)]

    #================================================================

    def __str__(self):
        s = f"P{self.ID} is located at ({self.x},{self.y}) and their status is '{self.statusRec()}'."
        return s
    

#================================================================================================================================================

def distanceFormula(A, B):
    return math.sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)

def distanceFormulaIndirect(A, B, index):
    return math.sqrt((A.x - B.spotX[index]) ** 2 + (A.y - B.spotY[index]) ** 2)

#================================================================

def transmission(popSet, fixed = None):

    n = len(popSet)

    if fixed == None:

        for i in range(0, n):
            for j in range(i + 1, n):

                if popSet[i].status + popSet[j].status == 7:
                    dist = distanceFormula(popSet[i], popSet[j])

                    if dist < InfectionDist:
                        if probability.infectionProbability(dist, InfectionDist, MaskFilter = MaskStatus, GloveFilter = GloveStatus):

                            if popSet[i].status == 2:
                                popSet[i].infect()
                                transmission(popSet, i)                                             # Recursively checking against new infection. 
                            
                            elif popSet[j].status == 2:
                                popSet[j].infect()
                                transmission(popSet, j)                                             # Recursively checking against new infection.
                            
                    
    else:

        for j in range(0, n):

            if popSet[j].status == 2:
                dist = distanceFormula(popSet[fixed], popSet[j])

                if dist < InfectionDist:
                    if probability.infectionProbability(dist, InfectionDist, MaskFilter = MaskStatus, GloveFilter = GloveStatus):

                        popSet[j].infect()
                        transmission(popSet, j)
                        
#================================================================

def spotTransmission(popSet):

    n = len(popSet)

    for i in range(0, n):
        if popSet[i].status == 2:

            for j in range(0, n):
                if popSet[j].status == 5:

                    for s in range(len(popSet[j].spotRecTime)):
                        dist = distanceFormulaIndirect(popSet[i], popSet[j], s)
                        
                        if dist < spotInfectionDist:

                            popSet[i].infect()
                            break
                    

#================================================================================================================================================

H = [Human() for n in range(0, population)]

#================================================================

initialInfection = random.sample(H, initialInfected)
for human in initialInfection:
    human.infect()

data = open("data.txt", "w")
data.write(f"0,{population - initialInfected},{initialInfected},0\n")                               #SIR
data.close()

#================================================================================================================================================

import turtle
import time

t = turtle.Turtle()
t.hideturtle()
turtle.Screen().tracer(0, 0)
turtle.Screen().setup(width = 550 , height = 600)

HumanSize = 3

# The graph is full of squares and recatangles, so:
def quadilateral(posx, posy, l, b):
  
    t.penup()
    t.setpos(posx, posy)
    t.pendown()
    t.setheading(0)
    for i in range(4):
        if i % 2 == 0:
            t.forward(l)
            t.right(90)
        else:
            t.forward(b)
            t.right(90)

def person_plotter(popSet, day, days):
  
    #For animation:
    t.clear()

    # Drawing the graph area:
    t.pensize(3)
    t.pencolor("black")
    quadilateral(-255,290,510,510)

    # Drawing a progress bar area:
    quadilateral(-255, -245, 510, 30)


    # Drawing the progress bar:
    t.pensize(1)
    t.color("lightgreen")
    t.begin_fill()
    quadilateral(-253, -247, (506/days) * (day+1), 26)
    t.end_fill()
    t.color("black")


    for human in popSet:

        t.penup()
        t.setpos((human.prevx * 500 / WORLD) - 251, (human.prevy * 500 / WORLD) - 216)
        t.pendown()
        t.pencolor("#D3D3D3")
        t.setpos((human.x * 500 / WORLD) - 251, (human.y * 500 / WORLD) - 216)
        t.pendown()

        if human.status == 5:
            t.pencolor("red")
        elif human.status == 2:
            t.pencolor("blue")
        elif human.status == 0:
            t.pencolor("green")
        else:
            t.pencolor("black")

        t.dot(HumanSize)

    turtle.Screen().update()
    time.sleep(0.1)

#================================================================================================================================================

def DayMovements(MoveNumber, day):

    for m in range(MoveNumber):

        for human in H:
            if human.status != -1:
                if human.movementNumber > m:
                    human.moveSimulation()
        transmission(H)
        if GloveStatus == False:
            spotTransmission(H)
        H[0].updateSusceptible()
        person_plotter(H, day, Days)

def toHomeMovements(day):
    
    for human in H:
        if human.status != -1:
            human.moveHome()
    transmission(H)
    if GloveStatus == False:
        spotTransmission(H)
    H[0].updateSusceptible()
    person_plotter(H, day, Days)

#================================================================

for day in trange(Days, file = sys.stdout, desc = "Days"):

    DayMovements(MAX_Moves, day)
    toHomeMovements(day)

    data = open("data.txt", "a")
    data.write(f"{day + 1},{H[0].counter[2]},{H[0].counter[3]},{H[0].counter[4]}\n")
    data.close()

#================================================================

print("")
print(f"Total Infections: {H[0].counter[1]} ---> {100 * H[0].counter[1] / population}% (Infection Rate)\n")
print(f"Susceptible: {H[0].counter[2]} ---> {100 * H[0].counter[2] / population}% (Non-Infected Percentage)\n")
print(f"Active Infections: {H[0].counter[3]} ---> {100 * H[0].counter[3] / population}% (Current Infected Rate)\n")
print(f"Recovered: {H[0].counter[4]} ---> {100 * H[0].counter[4] / H[0].counter[1]}% (Recovery Rate)\n")
print(f"Dead: {H[0].counter[5]} ---> {100 * H[0].counter[5] / H[0].counter[1]}% (Death Rate)\n")

#================================================================
minReach = Days

readData = open("data.txt", "r")
for line in readData.readlines():
    d,t,a,r = line.split(",")
    if int(a) == 0:
        minReach = d
        break

#================================================================

afterData = open("afterData.csv","a")
afterData.write(f"{Days},{WORLD},{population},{(1000 * 1000) * population/(WORLD * WORLD)},{H[0].counter[1]},{H[0].counter[3]},{H[0].counter[5]},{minReach} days,{MaskStatus},{GloveStatus},{LockdownStatus}\n")
afterData.close()

turtle.Screen().update()
turtle.done()