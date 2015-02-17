#/usr/bin/env python
# Script which goes with comb_description package.
# Load simple 'robot' point-cylinder and comb-obstacle to test methods.

from hpp.corbaserver.robot_2d_comb import Robot
from hpp.corbaserver import ProblemSolver
from hpp.corbaserver import Client
import time
import matplotlib.pyplot as plt

robot = Robot ('robot_2d_comb')
ps = ProblemSolver (robot)
cl = robot.client
cl.obstacle.loadObstacleModel('comb_description','comb_obstacle','')
#cl.obstacle.loadObstacleModel('comb_description','broken_comb_obstacle','')


from hpp.gepetto import Viewer, PathPlayer
Viewer.withFloor = True
r = Viewer (ps)
pp = PathPlayer (cl, r)
r.loadObstacleModel ("comb_description","comb_obstacle","comb_obstacle")
#r.loadObstacleModel ("comb_description","broken_comb_obstacle","broken_comb_obstacle")


# q = [x, y] # limits in URDF file
q1 = [0, -4.5]; q2 = [0, 4.5]
cl.problem.setInitialConfig (q1); cl.problem.addGoalConfig (q2); cl.problem.solve ()
begin=time.time()
cl.problem.optimizePath(0)
end=time.time()
print "Optim time: "+str(end-begin)


len(cl.problem.nodes ())
cl.problem.pathLength(0)
cl.problem.pathLength(1)


## Debug Optimization Tools ##############

import matplotlib.pyplot as plt
num_log = 31108
from parseLog import parseNodes, parsePathVector
from mutable_trajectory_plot import planarPlot, addNodePlot, addPathPlot

collConstrNodes = parseNodes (num_log, 'INFO:/local/mcampana/devel/hpp/src/hpp-core/src/path-optimization/gradient-based.cc:189: qCollConstr = ')
collNodes = parseNodes (num_log, 'INFO:/local/mcampana/devel/hpp/src/hpp-core/src/path-optimization/gradient-based.cc:183: qColl = ')

x1initLine = 'INFO:/local/mcampana/devel/hpp/src/hpp-core/src/path-optimization/gradient-based.cc:146: x0+alpha*p -> x1='
x1finishLine = 'INFO:/local/mcampana/devel/hpp/src/hpp-core/src/path-optimization/gradient-based.cc:148: finish path parsing'
x0Path = parsePathVector (num_log, x1initLine, x1finishLine, 1, 0)
x1Path = parsePathVector (num_log, x1initLine, x1finishLine, 2, 0)
x2Path = parsePathVector (num_log, x1initLine, x1finishLine, 3, 0)
x3Path = parsePathVector (num_log, x1initLine, x1finishLine, 4, 0)
x4Path = parsePathVector (num_log, x1initLine, x1finishLine, 5, 0)
x5Path = parsePathVector (num_log, x1initLine, x1finishLine, 6, 0)

plt = planarPlot (cl, 0, 1, plt, 5) # initialize 2D plot with obstacles and path
plt = addNodePlot (collConstrNodes, 'bo', 'qConstr', plt)
plt = addNodePlot (collNodes, 'ro', 'qCol', plt)
plt = addPathPlot (cl, x0Path, 'm', 1, plt)
plt = addPathPlot (cl, x1Path, 'g', 1, plt)
plt = addPathPlot (cl, x2Path, 'b', 1, plt)
plt = addPathPlot (cl, x3Path, 'y', 1, plt)
plt = addPathPlot (cl, x4Path, 'c', 1, plt)
plt = addPathPlot (cl, x5Path, '0.75', 1, plt)
plt.show() # will reset plt

#####################################################################

## DEBUG commands
cl.robot.setCurrentConfig(q2)
cl.robot.collisionTest()
cl.robot.distancesToCollision()
from numpy import *
argmin(cl.robot.distancesToCollision()[0])
r( cl.problem.configAtDistance(0,5) )
cl.problem.optimizePath (0)
cl.problem.clearRoadmap ()
cl.problem.resetGoalConfigs ()

