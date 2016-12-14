import numpy as np
import pylab as pl
import matplotlib.cm as cm
from sklearn.preprocessing import normalize

np.set_printoptions(threshold=np.inf)

#opened file and read lines into edges array
file = open('physics_collaboration_net.txt' , 'r')
edges=file.readlines();

#initialize expansion and inflation
expansion=4
inflation=2

count=0

noOfEdges=edges.__len__()

nodes={}

#splitting first row to get the nodes and added to nodes dictionary
for i in range (0, noOfEdges):
    node=edges[i].split()
    for j in range (0, node.__len__()):
        if (node[j] not in nodes):
            nodes[node[j]]=count
            count=count+1


#create associated matrix
AssocMatrix=np.zeros((count,count), dtype=np.float64)

for i in range (0, noOfEdges):
    node=edges[i].split()
    AssocMatrix[nodes[node[1]]][nodes[node[0]]]=1
    AssocMatrix[nodes[node[0]]][nodes[node[1]]]=1

#add self loops in associated matrix
for i in range (0, count):
    AssocMatrix[i][i]=1

#normalize the associated matrix
AssocMatrix=normalize(AssocMatrix, norm='l1', axis=0, copy=False)

#loop through the associated matrix and run expansion, inflation, normalization and check for convergence
isConverged=False

while (not isConverged):
    for i in range (0,expansion):
        AssocMatrix=np.dot(AssocMatrix, AssocMatrix)

    AssocMatrix=np.power(AssocMatrix, inflation)

    AssocMatrix=normalize(AssocMatrix, norm='l1', axis=0, copy=False)

    isConverged=True
    for j in range (0, count):
        value=0
        for i in range (0, count):
            if(AssocMatrix[i][j]<0.01):
               AssocMatrix[i][j]=0
            elif (AssocMatrix[i][j]>0 and value==0):
                value=AssocMatrix[i][j]
            elif(AssocMatrix[i][j]!=value):
                isConverged=False

    if(isConverged):
        break

#create clusters from steady state associated matrix
clusters=[]

for i in range (0, count):
    currcluster=[]
    for j in range (0, count):
        if(AssocMatrix[i][j]>0):
            currcluster.append(j)
    if (currcluster in clusters):
        continue

    clusters.append(currcluster)

print clusters

#add cluster number for each node
node_cluster={}

clusternumber=-1

for i in range (0, clusters.__len__()):
    onecluster=clusters[i]
    clusternumber=clusternumber+1
    for j in range (0, onecluster.__len__()):
        for key, value in nodes.iteritems():
            if ( value == onecluster[j] ):
                node_cluster[key]=clusternumber
                #print key, value, clusternumber
                del nodes[key]
                break


#add final cluster number in the clu file in the order of vertices found in .net file
file = open('physics_collaboration_net.net' , 'r')
dotnet=file.readlines();


fl=open('physics_collaboration_net.clu', 'w+')
s=dotnet[0]
fl.write(s)

for i in range (1, count+1):
    vertices=dotnet[i].split()
    key=vertices[1].replace("\"", "" )
    value=node_cluster[key]
    #print key, value
    value=str(value)
    fl.write(value)
    fl.write('\n')

fl.close()
