# Augmented, Randomized Diamond Square Algorithm implementation
# Written by Eirik Vesterkjær, Dec 2017
#
# This is a modified version of the diamond square algorithm.
# The reason it was written, was to use a DS-like algorithm for arrays with side lengths
# that are not 2^n + 1
# It accepts (non-jagged) 2D arrays of any (sensible) side lengths.
# It uses randomization to select indexes, and interpolation when a nx1 length remains unfilled.
# Print/plot functions are also supplied. Plotting requires matplotlib and numpy.


import random

HEIGHT_VARIATION_FACTOR = 0.2       # Magnitude of height deviations
RANDOMIZATION_SCALE_FACTOR = 0.2    # Magnitude of random index variations

"""
Prints a world heightmap.
@arg world_map: 2d array, heightmap.
"""
def printWorld(world_map):
    ylength = len(world_map[0])
    counter = 0
    marks = ylength // 5
    # Index in y-axis
    print("    ", end="")
    for i in range(marks):
        print(str(i*5).ljust(15, '-'), end="")
    print("Y")

    for row in world_map:
        # Index in x-axis
        print(str(counter).ljust(4) if (counter % 5) == 0 else "|   ", end= "")
        counter += 1
        
        for elem in row:
            print(str(elem).ljust(3), end="")
        print()
    print("X")


"""
Plots a world heightmap.
@arg world_map: 2d array, heightmap.
"""
def plotWorld3D(world_map):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import numpy as np
    
    Y = [i for i in range(len(world_map   ))]
    X = [i for i in range(len(world_map[0]))]
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, world_map, cmap=cm.spectral,
                       linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # It seems numpy defines y as len(array), which is the opposite of what I have done.
    # So, numpy's x axis is my y axis - and vice versa
    plt.xlabel("Y Axis")
    plt.ylabel("X Axis")
    plt.show()




"""
Deviation of a value in the heightmap from the averages of the surrounding values.
HEIGHT_VARIATION_FACTOR determines the magnitude of the deviation.
@arg x0, y0, x1, y1: Coords of corners.
"""
def dev(x0, y0, x1, y1):
    return int(HEIGHT_VARIATION_FACTOR * random.randint(-max(x1-x0, y1-y0), max(x1-x0, y1-y0)))

"""
Returns a random index around the middle of i0 and i1.
The val RANDOMIZATION_SCALE_FACTOR determines how far from the midpoint the return index can deviate
If the factor is 1, we can get any index between i0 or i1 as return value
If it is 0, we can only get the midpoint
@arg i0,i1: Max/min indexes for a heightmap axis for this step.
"""
def randAugIndex(i0, i1):
    # Check the indexes
    if i0 == i1 or i1 < i0:
        return i0
    elif i0 + 1 == i1: # No index in between
        return i0
    elif i0 + 2 == i1: # Only one index in between
        return i0 + 1
    # Calc new index & assure it is between i0 and i1 (and not equal either)
    i = int(i0 + (RANDOMIZATION_SCALE_FACTOR * random.random() + 1)*(i1-i0)/2)
    if i == i0:
        i += 1 # We know there is at least two indexes between i0 and i1
    elif i == i1:
        i -= 1 # ^

    return i

"""
Square step of the DS Algorithm.
Sets height values of 4 cells, which are the corners of next step's four diamond calls.
@arg world_map: 2D non-jagged array representing a heightmap
@arg x0,y0,x1,y1: Coordinates for corners (delimiters) of the area we're modifying 
                  in this step.
@arg i,j: Coordinates for the centre of the area, which is also a corner of the areas of the next step
"""
def Square(world_map, x0, y0, x1, y1, i, j):
    deviation =  dev(y0, y0, y1, y1) # = randint(-(y1-y0), (y1-y0)), where y1-y0 is the side length
    world_map[x0][j] = deviation + int(( world_map[x0][y0] + world_map[x0][y1] + world_map[i][j] ) / 3 )
    deviation =  dev(y0, y0, y1, y1)
    world_map[x1][j] = deviation + int(( world_map[x1][y0] + world_map[x1][y1] + world_map[i][j] ) / 3 )
    deviation =  dev(x0, x0, x1, x1)
    world_map[i][y0] = deviation + int(( world_map[x0][y0] + world_map[x1][y0] + world_map[i][j] ) / 3 )
    deviation =  dev(x0, x0, x1, x1)
    world_map[i][y1] = deviation + int(( world_map[x0][y1] + world_map[x1][y1] + world_map[i][j] ) / 3 )
    return

"""
Diamond step of the DS Algorithm.
Sets the centre of the heightmap equal to the average of the corners, plus a random deviation.
@arg world_map: 2D non-jagged array representing a heightmap
@arg x0,y0,x1,y1: Coordinates for corners (delimiters) of the area we're modifying 
                  in this step.
@arg i,j: Coordinates for the centre of the area, which is also a corner of the areas of the next step
"""
def Diamond(world_map, x0, y0, x1, y1, i, j):
    # Test here what kinds of terrain max & min give!
    deviation = dev(x0, y0, x1, y1)
    world_map[i][j] = deviation + int(( world_map[x0][y0] + world_map[x1][y0] + world_map[x0][y1] + world_map[x1][y1] ) / 4)
    return

"""
The actual implementation of the DS algo.
The coordinate arguments are two corners of the square part of the algorithm.
@arg world_map: 2D non-jagged array representing a heightmap
@arg x0,y0,x1,y1: Coordinates for corners (delimiters) of the area we're modifying 
                  in this step.
"""
def auxRandAugDS(world_map, x0, y0, x1, y1):
    if x0 == x1 and y0 == y1:
        return

    i = randAugIndex(x0, x1)
    j = randAugIndex(y0, y1)
    
    if   i == x0 or i == x1:
        for y in range(y0 + 1, y1):
            # Interpolation - creates a slope. Then returns.
            world_map[i][y] = int (world_map[i][y0] + (world_map[i][y1] - world_map[i][y0]) * (y - y0) / (y1 - y0))
            world_map[i][y] = int (world_map[i][y0] + (world_map[i][y1] - world_map[i][y0]) * (y - y0) / (y1 - y0))
        return
    elif j == y0 or j == y1: 
        for x in range(x0 + 1, x1):
            # Interpolation - creates a slope. Then returns.
            world_map[x][j] = int (world_map[x0][j] + (world_map[x0][j] - world_map[x1][j]) * (x - x0) / (x1 - x0))
            world_map[x][j] = int (world_map[x0][j] + (world_map[x0][j] - world_map[x1][j]) * (x - x0) / (x1 - x0))
        return

    # This step:
    Diamond(world_map, x0, y0, x1, y1, i, j)
    Square (world_map, x0, y0, x1, y1, i, j)

    # Next step:
    auxRandAugDS(world_map, x0, y0, i, j)
    auxRandAugDS(world_map, x0, j, i, y1)
    auxRandAugDS(world_map, i, y0, x1, j)
    auxRandAugDS(world_map, i, j, x1, y1)


"""
Cleans up the edges of the heightmap.
Due to some bug I haven't found so far, a few cells at the edges remain 0 after 
running the auxRandAugDS. Happens when calling randAugDS(m, 0) where m is a 40x40 array, for instance.
This function solves that problem!
@arg world_map: (Almost) finished, filled heightmap. 2D non-jagged array.
"""
def edgeCleanup(world_map):
    for x in range(len(world_map)):
        if world_map[x][0] == 0:
            if 0 < x < len(world_map) - 1:
                world_map[x][0] = int((world_map[x-1][0] + world_map[x][1] + world_map[x+1][0]) / 3)
        if world_map[x][-1] == 0:
            if 0 < x < len(world_map) - 1:
                world_map[x][-1] = int((world_map[x-1][-1] + world_map[x][-2] + world_map[x+1][-1]) / 3)

    for y in range(len(world_map[0])):
        if world_map[0][y] == 0:
            if 0 < y < len(world_map[0]) - 1:
                world_map[0][y] = int((world_map[0][y-1] + world_map[1][y] + world_map[0][y+1]) / 3)
        if world_map[-1][y] == 0:
            if 0 < y < len(world_map[0]) - 1:
                world_map[-1][y] = int((world_map[-1][y-1] + world_map[-2][y] + world_map[-1][y+1]) / 3)


"""
Randomized, augmented Diamond Square algorithm. 
Can be used on any array sizes and dimensions: Squares, rectangles, etc.
Initializes corner values & calls a recursive helper function.
@arg world_map: Uninitialized heightmap. 2D non-jagged array.
@arg seed: PRNG seed used for randomization and terrain variations
"""
def randAugDS(world_map, seed):
    random.seed(seed)
    
    x0 = 0
    x1 = len(world_map) - 1
    y0 = 0
    y1 = len(world_map[0]) - 1

    # Initialize corners
    world_map[x0][y0] = random.randint(0, max(x1, y1))
    world_map[x0][y1] = random.randint(0, max(x1, y1))
    world_map[x1][y0] = random.randint(0, max(x1, y1))
    world_map[x1][y1] = random.randint(0, max(x1, y1))

    # Call algorithm
    auxRandAugDS(world_map, x0, y0, x1, y1)

    # Clean up any cells not modified by the algorithm (which only happens for some heightmap dimensions)
    edgeCleanup(world_map)

    return world_map




"""
Usage example for randAugDS(world_map, seed)
"""
def exampleCall():

    # Do use 0 as initial values for the heightmap! 
    # This is necessary for edgeCleanup(world_map) to work correctly.
    m = [[0 for j in range(45)] for i in range(25)]

    # Prints in terminal
    printWorld(randAugDS(m, 2))

    plotWorld3D(m)

