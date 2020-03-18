# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:07:48 2020

@author: mtrent
"""

#Question 1
#Read in the data
import pandas as pd

commData = pd.read_csv("communicationHistory.csv",header=None, names=['from', 'to', 'duration'])

directors = [12, 17, 5, 11, 4]

# I don't want to assume that the list of caller i.e. "from" is a continuous 
#list from 0 to 49, so I'll compile a list of unique callers

callsFrom = commData.iloc[:,0] # Gather all callers
callers = [] #Initialize the set of unique callers
for caller in callsFrom:
    if caller not in callers:
        callers.append(caller)

# now we need to establish the recipients for each caller 
#(ie the connections)
calls = [] #initialize the calls list

#For each caller, we need to iterate through the list of possible
#recipients to determine if a call was made between the caller and 
#that recipient

for caller in callers:
    for recipient in range(0,len(commData.iloc[:,1])):
        #print("Caller is ", str(caller), " recipient is ", str(commData.iloc[i,1]))
        if commData.iloc[recipient, 0] == caller:
            call = [caller, commData.iloc[recipient,1]]
            #print(call)
            if call not in calls:
                calls.append(call)
#Now that we have a list of unique calls, we need to determine the 
#inverse of the volume. This is done by calculating a running total
#of the durations of all of the calls 
callData = {} #initialize the dictionary for the callData
for caller in callers:
    callData[caller]={}
    for call in calls:
        callVol = 0
        for recipient in range(0,len(commData.iloc[:,1])):
            if commData.iloc[recipient, 0] == caller and commData.iloc[recipient,1] == call[1]:
                callVol = callVol + commData.iloc[recipient,2]
            if callVol > 0:
                callData[caller][call[1]] = 1/callVol
#%% Part B. Run through Dijksra's algorithm for each board member

leaker = 22
shortestPath = []
paths = []
for member in directors:
    shortPath, path = Dijkstra(callData, member, leaker)
    shortestPath.append(shortPath)
    path.append(path)

pathsToLeaker = dict(zip(directors,shortestPath))


#%%             
# Define Dijkstras Algorithm
                
def Dijkstra(G,s,t):
    dist={} #dist[i] is the shortest known distance from s to i.
    prev={} #prev[i]=j means that vertex j immediately precedes vertex i on the shortest known path from s to i..
    visited=[] #set of vertices that have already appeared at the top of the Q and had all neighbors explored.  these vertices can be excluded from future queues.
    Q = G.keys() #initially all vertices may be part of the queue.
    
    for vertex in Q: #initializing shortest known distances.
        dist[vertex] = float("inf") #For each of the vertices that are in the
                            #queue, set the shortest distance to infinity
        prev[vertex] = None # For each of the vertices in Q set the previous 
        #                   #vertex to None (none have yet been visited)
    dist[s]=0 # The distance to the starting point from the starting point

    while(t not in visited): #while the current vertex is not within the set 
                        #   "visited" meaning we haven't been there before
        X = sorted(dist, key=dist.get) #sorts vertices according to value of 
                                    #dist.  (i.e. if dist[i] < dist[j], then i 
                                    #comes before j in the list X.)
        Q=[] #Create a new queue
        for x in X: # For each vertex in the sorted list, if we haven't already
                                #visited that vertex, then add it to the queue
            if(x not in visited):
                Q.append(x) # if the vertex hasn't been visted, 
                            #then add it to the queue
        currVertex=Q[0] #Set the current vertex to the first element of the 
                        #Queue (distance should be zero for this vertex)
        for neighbor in G[currVertex].keys():
            if(dist[neighbor] > dist[currVertex] + G[currVertex][neighbor]): 
                # For each neighbor in the adjacency matrix of the current 
                #vertex if the distance to that vertex is greater than the 
                #distance to the current vertex plus the distance between 
                #the current vertex and the neighbor then
                dist[neighbor] = dist[currVertex] + G[currVertex][neighbor] 
                # update the distance to the neighbors using the distance 
                #traveled thus far plus the distance to that neighbor
                prev[neighbor] = currVertex 
                #Add the current vertex to the previously prev for the neighbor
        visited.append(currVertex)#Add the current vertex to the set of visted vertices
    print('Tracing back the line of predecessors from the destination:') 
    cur = t #starting at the destination
    path = [] # Create an empty vector for the final path
    while(cur != s): #and until we get to the start location
        print('Vertex with index:') #string printing which vertex connected
        print(cur)
        path.append(cur)
        cur = prev[cur] #move from current vertex to predecessor.
    path.append(s) #Add the previous vertex to path
    path.reverse() #Reverse the path
    return dist[t], path