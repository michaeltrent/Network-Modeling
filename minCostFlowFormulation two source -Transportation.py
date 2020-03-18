# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 02:24:29 2019

@author: poikones
"""


"""This code solves the maximum flow problem
for the example network that can be seen here:
    http://www.mathcs.emory.edu/~cheung/Courses/323/Syllabus/NetFlow/FIGS/LP/lp01.gif

The idea is that we would like to maximize the total flow from vertex 0
to vertex 7, but we must respect the flow capacities on intermediate arcs.
"""
from gurobipy import *

"""Problem inputs"""
#Setting up a dictionary with arc capacity
#If an arc from (i,j) has capacity of k, then
#caps[(i,j)] = k
caps = {}
caps[(0,1)]=5
caps[(0,2)]=5
caps[(1,4)]=5
caps[(1,5)]=5
caps[(3,2)]=5
caps[(2,3)]=5
caps[(2,4)]=5
caps[(3,4)]=5
caps[(4,6)]=5
caps[(5,6)]=5

cost = {}
cost[(0,1)]=4
cost[(0,2)]=3
cost[(1,4)]=12
cost[(1,5)]=5
cost[(3,2)]=7
cost[(2,3)]=7
cost[(2,4)]=10
cost[(3,4)]=2
cost[(4,6)]=5
cost[(5,6)]=16

#This creates a list of all arcs in the problem.
arcs = caps.keys()


"""Creating the model"""
#Let's create a Gurobi model called m.
m = Model()

#We would like to maximize flow from vertex 0 to vertex 7.
#So let's indicate that we are  minimizing.
m.ModelSense = GRB.MINIMIZE



"""Declaring decision variables"""
#We would like to have a decision variable for each arc.
#In particular, we would like to choose how much flow
#we have across each arc.

#x[(i,j)] will represent the how much flow we choose to
#send from vertex i to vertex j.

x={} #Let's start by creating an empty dictionary for x.

for arc in arcs: #For each arc
    
    #Create a decision variable called x[arc].
    #We set the variable type to CONTINUOUS.
    #The flow along this arc does not actually affect
    #the objective value.  So we set obj=0.  This is the
    #coefficient in front of the variable in the objective
    #function.
    x[arc] = m.addVar(vtype=GRB.CONTINUOUS,name='x'+str(arc),obj=cost[arc])
    y[arc] = m.addVar(vtype=GRB.CONTINUOUS, name ='y'+str(arc), obj = cost[arc])
    
#We wish to create another variable that measures flow
#into vertex 7, which is our destination.
#In this case, obj=1.  This is the coefficient
#in front of this variable in the objective function.
#Remember, we want to maximize flow into the destination,
#so we ware maximizing 1 * (flow into destination).
intoDestinationx = m.addVar(vtype=GRB.CONTINUOUS,obj=0,name='intoDestinationx')
intoDestinationy = m.addVar(vtype=GRB.CONTINUOUS,obj=0,name='intoDestinationy')


"""Adding constraints to the model"""
#Capacity constraints
#The decision variable x[arc] <= caps[arc]
#In other words, chosen flow across the arc
#must be less than arc maximum capacity.
for arc in arcs:
    m.addConstr(x[arc] + y[arc],GRB.LESS_EQUAL,5)

#Flow conservation constraints
#flow into a vertex must be equal to flow out of vertex
#except for source (vertex 0) and sink (vertex 7)
m.addConstr(x[(0,1)],GRB.EQUAL,x[(1,4)]+x[(1,5)]) #vertex 1
m.addConstr(y[(0,1)],GRB.EQUAL,y[(1,4)]+y[(1,5)]) #vertex 1
m.addConstr(x[(2,4)],GRB.EQUAL,x[(3,2)]+x[(0,2)]) #vertex 2 source 2 & 1
m.addConstr(y[(2,4)],GRB.EQUAL,y[(3,2)]+y[(0,2)]) #vertex 2 source 2 & 1
m.addConstr(x[(1,4)]+x[(2,4)]+x[(3,4)],GRB.EQUAL,x[(4,6)]) #vertex 4
m.addConstr(y[(1,4)]+y[(2,4)]+y[(3,4)],GRB.EQUAL,y[(4,6)]) #vertex 4
m.addConstr(x[(1,5)],GRB.EQUAL,x[(5,6)]) #vertex 5
m.addConstr(y[(1,5)],GRB.EQUAL,y[(5,6)]) #vertex 5

#add constraint to ensure 

m.addConstr(intoDestinationx,GRB.EQUAL,4)
m.addConstr(intoDestinationx,GRB.EQUAL,x[(4,6)]+x[(5,6)])
m.addConstr(intoDestinationy,GRB.EQUAL,2)
m.addConstr(intoDestinationy,GRB.EQUAL,y[(4,6)]+y[(5,6)])

"""Run the model and find an optimal solution, if possible."""
m.optimize()


"""Let's look at the results of the model."""
#m.objVal is the objective value found
#after the model is done optimizing.
print('Best objective value is:')
print(m.objVal)

#Let's get the list of all the decision variables in the model.
decisionVariables = m.getVars()

print('Values of decision variables:')
for var in decisionVariables:
    print('Var name:')
    print(var.VarName)
    print('Var value:')
    print(var.X)
    
#For any variable object, .VarName will return the variables name.
#If a variable name was not set, then some automatically generated
#variable name will show up.  (e.g. C12, meaning the 12th variable created.)
    

#For any variable object, .X will return the value chosen for that
#variable in the optimal solution.
