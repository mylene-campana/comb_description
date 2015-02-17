#/usr/bin/env python
# Author : Mylene Campana
# Script to plot some graphs after launching a corbaserver and solving 
# the problem. The main DIFFERENCE here is that the plot is always returned so that 
# plots can be added later in the Python interface.
# Use has to call himself "plt.show()"

#import matplotlib.pyplot as plt
from __future__ import division
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

dt = 0.02 # global drawing step size


# --------------------------------------------------------------------#

def planarPlot (cl, nPath0, nPath1, plt, lim):
    dx = 0.8 # comb parameter
    dl = 1.4
    dL = 0.4
    plt.gcf().gca().add_artist(plt.Rectangle((0-dl/2,0-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((dl/2,dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((0-dl/2,2*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((dl/2,3*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((0-dl/2,4*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((dl/2,5*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((dl/2,-1*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((0-dl/2,-2*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((dl/2,-3*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((0-dl/2,-4*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((dl/2,-5*dx-dL/2),dl,dL,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((-0.9-dL/2,0-8.4/2),dL,8.4,color='r'))
    plt.gcf().gca().add_artist(plt.Rectangle((2.2-dL/2,0-8.4/2),dL,8.4,color='r'))
    
    init = cl.problem.getInitialConfig ()
    goal = cl.problem.getGoalConfigs ()[0] # first goal
    """i = 0
    for n in cl.problem.nodes() :
        if i>1: # avoid 2 first nodes (init and goal)
            plt.plot(n[0], n[1], 'ro')
            plt.text(n[0]+.02, n[1], r'qNew%i' %(i), fontsize=8)
        i=i+1
    """
    for t in np.arange(0., cl.problem.pathLength(nPath1), dt):
        plt.plot([cl.problem.configAtParam(nPath1, t)[0], \
                     cl.problem.configAtParam(nPath1, t+dt)[0]], \
                     [cl.problem.configAtParam(nPath1, t)[1], \
                     cl.problem.configAtParam(nPath1, t+dt)[1]], 'k', linewidth=1.8, label="optim." if t == 0. else "")
    
    for t in np.arange(0., cl.problem.pathLength(nPath0), dt):
        plt.plot([cl.problem.configAtParam(nPath0, t)[0], \
                 cl.problem.configAtParam(nPath0, t+dt)[0]], \
                 [cl.problem.configAtParam(nPath0, t)[1], \
                 cl.problem.configAtParam(nPath0, t+dt)[1]], 'r', label="init." if t == 0. else "")
    
    plt.legend()
    plt.axis([-lim, lim, -lim, lim])
    plt.xlabel('x'); plt.ylabel('y')
    plt.title('trajectory'); plt.grid()
    plt.plot(init[0], init[1], 'go')
    plt.plot(goal[0], goal[1], 'go')
    plt.text(init[0]+.1, init[1]+.1, r'q_init', fontsize=11)
    plt.text(goal[0]+.1, goal[1]+.1, r'q_end', fontsize=11)
    return plt

# --------------------------------------------------------------------#

# Plot 2D nodes (from parseLog) with given color and text.
# For example, nodeName = r'qCol'    and   nodeColor = 'bo'
def addNodePlot (nodeList, nodeColor, nodeName, plt):
    i = 0
    for n in nodeList :
        plt.plot(n[0], n[1], nodeColor)
        plt.text(n[0]+.02, n[1], nodeName+'%i' %(i), fontsize=8)
        i = i+1
    return plt

# --------------------------------------------------------------------#

# Plot 2D trajectory (parsed from parseLog), with no label.
# For example, nodeName = r'qCol'    and   nodeColor = 'bo'
def addPathPlot (cl, path, pathColor, lw, plt):
    size = len(path) # number of lines = 2*nbSegments
    print "pathSize= "+str(size)
    init = cl.problem.getInitialConfig ()
    goal = cl.problem.getGoalConfigs ()[0] # first goal
    i = 0
    while(i < size-1):
        # plot segment
        plt.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], pathColor, linewidth=lw) 
        i = i+1 # go to next segment
    # Add first and last segment
    plt.plot([init[0], path[0][0]], [init[1], path[0][1]], pathColor, linewidth=lw)
    plt.plot([goal[0], path[size-1][0]], [goal[1], path[size-1][1]], pathColor, linewidth=lw)
    return plt

