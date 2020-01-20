# Python code to implement Conway's Game Of Life 
import argparse 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
from PIL import Image

# setting up the values for the grid 
ON = 255
OFF = 0
vals = [ON, OFF] 
BLACK_C = (255,255,255)
WHITE_C = (0,0,0)

def humanist(grid):
    #blank = np.zeros(N*N).reshape(N, N) 
    counter = 0
    SLATE = [['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','X','O','O','O','O','O','O','O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O'],
             ['O','O','O','X','O','O','O','O','O','O','O','O','O','O','X','O','O','O','O','O','O','O','O','O','O','O','O','O','O'],
             ['O','O','O','O','O','O','X','O','X','O','O','X','O','X','O','O','O','O','X','O','O','X','O','X','X','O','O','O','O'],
             ['O','O','O','O','X','X','O','X','O','X','X','O','O','X','O','X','X','X','X','O','X','X','O','O','X','O','O','O','O'],
             ['O','O','O','O','X','O','X','O','X','O','X','O','X','O','O','O','O','O','X','O','X','X','O','X','O','O','O','O','O'],
             ['O','O','X','O','X','O','O','O','O','O','X','O','O','O','O','O','X','X','O','O','O','O','O','O','O','X','O','O','O'],
             ['O','O','O','O','X','X','O','X','O','X','X','O','X','X','O','O','X','O','X','O','X','O','O','X','O','O','O','O','O'],
             ['O','O','O','O','X','O','X','O','X','O','X','O','X','O','X','X','O','O','X','X','O','X','X','O','O','X','O','O','O'],
             ['O','O','O','O','O','X','O','X','O','X','O','O','O','O','X','O','O','O','X','O','O','X','X','O','X','O','O','O','O'],
             ['O','O','O','O','X','O','O','O','O','O','X','O','X','X','O','O','X','X','O','O','O','O','O','O','O','X','X','X','O'],
             ['O','O','O','O','O','O','O','O','X','X','X','X','O','O','O','X','O','X','X','O','O','X','X','O','X','X','O','X','O'],
             ['O','O','O','X','O','X','O','O','X','O','O','O','O','O','O','X','O','O','O','X','X','O','O','O','O','O','X','O','O'],
             ['O','O','O','O','O','O','X','X','X','O','O','X','O','X','X','O','O','O','X','O','O','X','X','O','X','O','X','X','O'],
             ['O','O','O','X','O','X','O','O','X','X','O','X','X','O','O','O','X','O','O','O','O','O','O','X','O','O','X','X','O'],
             ['O','O','O','O','X','O','X','X','X','X','O','O','O','X','X','O','X','O','O','X','X','X','X','O','O','O','X','O','O'],
             ['O','O','O','O','O','O','X','X','O','O','O','O','O','O','X','X','O','O','X','O','X','O','X','O','X','O','X','X','O'],
             ['O','O','O','O','O','X','O','O','X','X','O','O','X','X','X','O','O','X','O','X','O','X','O','X','X','O','X','X','O'],
             ['O','O','O','X','X','O','O','O','O','X','X','O','O','X','O','X','O','O','O','O','X','O','O','O','X','O','O','X','O'],
             ['O','O','O','O','O','O','O','X','O','O','X','O','X','O','O','O','X','O','X','X','O','O','O','O','O','O','X','X','O'],
             ['O','X','X','X','O','O','X','X','O','O','X','O','O','X','X','O','O','O','X','O','O','X','X','X','X','O','X','X','O'],
             ['O','O','X','X','X','O','O','X','O','O','O','X','O','X','X','X','O','X','O','O','O','X','O','X','O','O','X','O','O'],
             ['O','X','O','O','O','O','O','O','O','X','O','O','O','X','O','O','O','O','X','X','O','X','O','O','X','O','X','X','O'],
             ['O','X','O','O','X','O','O','O','O','O','O','X','O','O','X','O','O','O','O','X','X','O','O','O','O','X','X','O','O'],
             ['O','X','O','X','O','X','X','X','X','O','X','O','O','X','X','X','X','X','X','X','O','O','X','X','O','O','X','O','O'],
             ['O','X','O','O','O','X','X','X','X','X','X','X','O','X','X','O','X','X','O','O','X','X','X','X','X','X','X','O','O'],
             ['O','O','O','X','O','O','X','O','O','O','O','X','X','X','X','O','O','X','X','X','O','X','O','X','O','O','X','X','O'],
             ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O'],
             ]
    row_count = 0
    col_count = 0
    for r in grid:
        #print SLATE[row_count]
        col_count = 0
        for c in r:            
            if SLATE[row_count][col_count] is 'O':
                grid[row_count][col_count] = OFF
            else:
                grid[row_count][col_count] = ON
            col_count += 1
        row_count += 1
    #print grid
    

def randomGrid(N): 

    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N) 

def addGlider(i, j, grid): 

    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255], 
                    [255, 0, 255], 
                    [0, 255, 255]]) 
    grid[i:i+3, j:j+3] = glider 

def addGosperGliderGun(i, j, grid): 

    """adds a Gosper Glider Gun with top left 
    cell at (i, j)"""
    gun = np.zeros(11*38).reshape(11, 38) 

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i+11, j:j+38] = gun 

def update(frameNum, grid, N): 
    print "Calculating: %d" % int(frameNum)
    # copy grid since we require 8 neighbors 
    # for calculation and we go line by line 
    newGrid = grid.copy() 
    for i in range(N): 
        print "Row: %d" % i
        for j in range(N): 

            # compute 8-neghbor sum 
            # using toroidal boundary conditions - x and y wrap around 
            # so that the simulaton takes place on a toroidal surface. 
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255) 
            #if i == 7 and j == 7:
            #print total            
            #print total
            # apply Conway's rules 
            if grid[i, j] == ON: 
                if (total < 2):
                    newGrid[i, j] = OFF 
                elif (total > 3):
                    newGrid[i, j] = OFF 
                elif (total == 2) or (total == 3):
                    #print "i = %d, j = %d total = %d" % (i,j,total) 
                    newGrid[i, j] = ON
            elif grid[i,j] == OFF: 
                if total == 3: 
                    newGrid[i, j] = ON 
                    #print "i = %d, j = %d total = %d" % (i,j,total) 
            #raw_input()
            
    # update data 
    #img.set_data(newGrid) 
    grid[:] = newGrid[:]
    s = ""
    r_count = 0
    c_count = 0
    for r in grid:
        c_count = 0
        for c in r:            
            if grid[r_count][c_count] == 255:
                s = s + 'X'
            else:
                s = s + 'O'
            c_count += 1
        s = s + '\n'
        r_count += 1
    print s
    output = Image.new('RGB',(29,29), 'grey')
    r_count = 0
    c_count = 0
    for r in grid:
        c_count = 0
        for c in r:            
            if grid[r_count][c_count] == 255.0:
                output.putpixel((c_count,r_count), WHITE_C)
            else:
                output.putpixel((c_count,r_count), BLACK_C)
            c_count += 1
        r_count += 1
    output.save('FRAME_%04d.png'%(int(frameNum)))
    
    return grid, 

# main() function 
def main(): 

    # Command line args are in sys.argv[1], sys.argv[2] .. 
    # sys.argv[0] is the script name itself and can be ignored 
    # parse arguments 
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.") 

    # add arguments 
    parser.add_argument('--grid-size', dest='N', required=False) 
    parser.add_argument('--frames', dest='frames', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False) 
    parser.add_argument('--interval', dest='interval', required=False) 
    parser.add_argument('--glider', action='store_true', required=False) 
    parser.add_argument('--gosper', action='store_true', required=False) 
    parser.add_argument('--humanist', action='store_true', required=False)
    args = parser.parse_args() 
    
    code = Image.new('RGB',(29,29), 'grey')
    
    frames = 10
    
    # set grid size 
    N = 100
    if args.N and int(args.N) > 8: 
        N = int(args.N) 
        
    # set animation update interval 
    updateInterval = 1000
    if args.interval: 
        updateInterval = int(args.interval) 

    # declare grid 
    grid = np.array([]) 

    # check if "glider" demo flag is specified 
    if args.glider: 
        grid = np.zeros(N*N).reshape(N, N) 
        addGlider(1, 1, grid) 
    elif args.gosper: 
        grid = np.zeros(N*N).reshape(N, N) 
        addGosperGliderGun(10, 10, grid) 
    elif args.humanist:
        if N != 29:
            N = 29
        grid = np.zeros(N*N).reshape(N, N)
        humanist(grid)
    else: # populate grid with random on/off - 
            # more off than on 
        grid = randomGrid(N) 
    r_count = 0
    c_count = 0
    for r in grid:
        c_count = 0
        for c in r:     
            #print c_count
            if grid[r_count][c_count] == 255.0:
                code.putpixel((c_count,r_count), WHITE_C)
            else:
                code.putpixel((c_count,r_count), BLACK_C)
            c_count += 1
        r_count += 1
    code.save('inital.png')
    # set up animation 
    #fig, ax = plt.subplots() 
    #img = ax.imshow(grid, interpolation='nearest') 
    #ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), 
    #                            frames = 1, 
    #                            interval=updateInterval, 
    #                            save_count=50) 
    for i in range(frames):
        update(i, grid, N,)
    # # of frames? 
    # set output file 
    #if args.movfile: 
    #    ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264']) 

    plt.show() 

# call main 
if __name__ == '__main__': 
    main() 
