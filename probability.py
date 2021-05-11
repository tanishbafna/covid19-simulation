import random

#================================================================

def age():

    ageRanges = [0, 4, 9, 14, 19, 24, 44, 64, 79, 99]
    demographics = (0, 10.7, 12.5, 12.1, 9.7, 8.7, 27.6, 13.5, 4.0, 0.8)

    rangeUpper = ageRanges.index(random.choices(ageRanges, weights = demographics, k = 1)[0])
    rangeLower = rangeUpper - 1

    return random.randint(ageRanges[rangeLower] + 1, ageRanges[rangeUpper])

#================================================================

def IC(AGE):                                                                # IC = ImmunoCompromised

    ICRanges = [0, 9, 19, 29, 39, 49, 59, 69, 79, 99]
    ICchance = [0, 5, 3, 10, 15, 20, 23, 30, 40, 60]

    for i in range(1, len(ICRanges)):
        if ICRanges[i] >= AGE and ICRanges[i - 1] < AGE:
            tempChance = ICchance[i]
            break

    if random.randint(0, 100) <= tempChance:
        return True
    else:
        return False

#================================================================

def death(AGE, IC = False):                                     

    # With non-overlowing medicare
    deathRanges = [0, 9, 19, 29, 39, 49, 59, 69, 79, 99]

    if IC == False:
        deathChance = [0, 2, 2, 2, 3, 4, 6, 7, 8, 15, 25]    
    else:
        deathChance = [0, 20, 20, 25, 25, 30, 30, 35, 45, 60]

    for d in range(1, len(deathRanges)):
        if deathRanges[d] >= AGE and deathRanges[d - 1] < AGE:
            tempChance = deathChance[d]
            break

    if random.randint(0, 100) <= tempChance:
        return True
    else:
        return False

#================================================================

def time(AGE, IC, DEATH):

    ageRanges = [0, 9, 29, 49, 69, 99]

    if DEATH == False and IC == False:
        timeRange = [0, 15, 10, 15, 17, 18]
    elif DEATH == False and IC == True:
        timeRange = [0, 16, 15, 17, 18, 20]
    elif DEATH == True and IC == True:
        timeRange = [0, 10, 12, 10, 9, 8]
    else:
        timeRange = [0, 12, 16, 14, 12, 10] 

    for a in range(1, len(ageRanges)):
        if ageRanges[a] >= AGE and ageRanges[a - 1] < AGE:
            tempTime = timeRange[a]
            break

    return tempTime

#================================================================

def distanceBefore(AGE, worldSize, lockdown = False):
    
    ageRanges = [0, 9, 19, 29, 49, 69, 99]

    if lockdown == False:
        distBeforeRanges = [0, (3/50),(4/50), (4/50), (4.5/50), (3/50), (1.5/50)]
    else:
        distBeforeRanges = [0, (1/50),(2/50), (2.5/50), (2.5/50), (1.5/50), (0.75/50)]

    distBeforeRanges = [round(i * worldSize) for i in distBeforeRanges]

    for a in range(1, len(ageRanges)):
        if ageRanges[a] >= AGE and ageRanges[a - 1] < AGE:
            tempDistanceBefore = distBeforeRanges[a]
            break

    return tempDistanceBefore

#================================================================

def distanceAfter(AGE, IC, worldSize, lockdown = False):
    
    ageRanges = [0, 9, 19, 29, 49, 69, 99]

    if IC == False and lockdown == False:
        distAfterRanges = [0, (2/50), (3/50), (3.5/50), (2.5/50), (2/50), (1/50)]
    elif IC == True and lockdown == True:
        distAfterRanges = [0, (0.2/50), (0.5/50), (1/50), (1/50), (0.5/50), (0.1/50)]
    elif IC == True:
        distAfterRanges = [0, (1.5/50), (2/50), (2.5/50), (1.5/50), (1/50), (0.5/50)]
    elif lockdown == True:
        distAfterRanges = [0, (0.5/50), (1/50), (2/50), (2/50), (1.5/50), (0.5/50)]
    
    distAfterRanges = [round(i * worldSize) for i in distAfterRanges]

    for a in range(1, len(ageRanges)):
        if ageRanges[a] >= AGE and ageRanges[a - 1] < AGE:
            tempDistanceAfter = distAfterRanges[a]
            break

    return tempDistanceAfter

#================================================================

def infectionProbability(distance, infectionDistance, MaskFilter = False, GloveFilter = False):

    if MaskFilter == False and GloveFilter == False:
        prob = 1.30
    elif MaskFilter == True and GloveFilter == True:
        prob = 0.65
    elif MaskFilter == True:
        prob = 0.70
    elif GloveFilter == True:
        prob = 1.20

    tempProbability = (1 - (distance / infectionDistance)) * prob
    infectionChance = (tempProbability, 1 - tempProbability)
    infection = [True, False]

    return random.choices(infection, weights = infectionChance, k = 1)[0]

#================================================================

def movement(AGE, IC = False, lockdown = False):

    ageRanges = [0, 9, 49, 59, 69, 99]

    if IC == False and lockdown == False:
        movementRanges = [0, 1, 2, 2, 2, 1]                     # Number of places a person vistis before coming home.
    elif IC == True and lockdown == True:
        movementRanges = [0, 0, 1, 1, 0, 0]
    elif IC == True:
        movementRanges = [0, 1, 2, 2, 1, 0]
    elif lockdown == True:
        movementRanges = [0, 0, 1, 1, 1, 0]
    
    for a in range(1, len(ageRanges)):
        if ageRanges[a] >= AGE and ageRanges[a - 1] < AGE:
            tempDistanceNumber = movementRanges[a]
            break

    return tempDistanceNumber

#================================================================

def asymptomatic(AGE):

    ageRanges = [0, 9, 19, 29, 49, 69, 99]
    asympChance = [0, 8, 20, 18, 13, 8, 3]

    for i in range(1, len(ageRanges)):
        if ageRanges[i] >= AGE and ageRanges[i - 1] < AGE:
            tempChance = asympChance[i]
            break

    if random.randint(0, 100) <= tempChance:
        return True
    else:
        return False

#================================================================