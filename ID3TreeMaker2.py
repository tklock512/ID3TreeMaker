import sys
import math

#class that connects the name of a variable and the column it belongs to for the data
class variable:
    def __init__(self, name, column):
        self.name = name
        self.column = column

#class for a simple ternary tree
class treeNode:
    def __init__(self, a):
        self.z = None
        self.o = None
        self.t = None
        self.attribute = a
        self.classification = None

    def printTree(self, spaces):
        newSpaces = spaces+"| "

        
        print(spaces+self.attribute+" = 0:", end=" ")
        if self.z:
            if self.z.classification != None:
                print(self.z.classification)
            else:
                print("")
                self.z.printTree(newSpaces)
        else:
            print()

        
        print(spaces+self.attribute+" = 1:", end = " ")
        if self.o:
            if self.o.classification != None:
                print(self.o.classification)
            else:
                print("")
                self.o.printTree(newSpaces)
        else:
            print()

        print(spaces+self.attribute+" = 2:", end = " ")
        if self.t:
            if self.t.classification != None:
                print(self.t.classification)
            else:
                print("")
                self.t.printTree(newSpaces)
        else:
            print()

#function that performs log, but if 0 log 0 is performed it replaces it with 1 instead
def logZeroFixer(states, total):
    if states == 0:
        return 0
    else:
        return (states/total)*math.log(states/total, 2)

#function that calculates the entropy of a given set of data
def calc_entropy(data):
    total = len(data)
    if total == 0: #if there is no data
        return -1
    z_states = 0
    o_states = 0
    t_states = 0
    for x in data:
        if x[-1] == 0:
            o_states+=1
        if x[-1] == 1:
            z_states+=1
        if x[-1] == 2:
            t_states+=1
    z_ent = logZeroFixer(z_states, total)
    o_ent = logZeroFixer(o_states, total)
    t_ent = logZeroFixer(t_states, total)
    
    return -z_ent - o_ent - t_ent

#Finds the best Information Gain given the available columns (which variables are left to be used) and the provided data (For instance, if column 1 was used as the first node, then the given data would only be column 1: 0 or column 1: 1 or column 1: 2 and so on)
def findBestIGCol(colm, dataums, nEntropy):
    IG = []
    if len(dataums) == 0:
        print("data is 0")
    for c in colm:
        col = c.column
        zDataForC = []
        for d in dataums:
            if d[col] == 0:
                zDataForC.append(d)
        zEntropy = calc_entropy(zDataForC)
        oDataForC = []
        for d in dataums:
            if d[col] == 1:
                oDataForC.append(d)
        oEntropy = calc_entropy(oDataForC)
        tDataForC = []
        for d in dataums:
            if d[col] == 2:
                tDataForC.append(d)
        tEntropy = calc_entropy(tDataForC)

        infoGain = nEntropy-(zEntropy*(len(zDataForC)/len(dataums)))-(oEntropy*(len(oDataForC)/len(dataums)))-(tEntropy*(len(tDataForC)/len(dataums)))
        IG.append(infoGain)
    
    best = max(IG) 
    return IG.index(best)

def mostCommon(dat):
    zCount = 0
    oCount = 0
    tCount = 0
    
    for d in dat:
        if d[-1] == 0:
            zCount+=1
        if d[-1] == 1:
            oCount+=1
        if d[-1] == 2:
            tCount+=1
    ar = [zCount, oCount, tCount]
    return ar.index(max(ar))

#function for checking if given column and data set is a leaf node
def checkLeaf(cls, dts):
    ent = calc_entropy(dts)
    
    if len(dts) == 0:
        return mostCommon(allData)

    if ent == 0: #if the node does not have any entropy i.e it is pure
        d = dts[0]
        clss = d[-1]
        return clss

    if len(cls) == 0: #there are no more variables to further seperate data
        return mostCommon(dts)

    return None

#Function for making the ID3 Tree
def treeMaker(cols, datas):

    nodeEntropy = calc_entropy(datas)

    if len(datas) == 0:
        return None

    if nodeEntropy == 0: #if the node does not have any entropy i.e it is pure
        return None

    if len(cols) == 0: #there are no more variables to further seperate data
        return None

    bestIG = findBestIGCol(cols, datas, nodeEntropy)
    bestColumn = None
    newNode = None
    loweredColumns = []

    for i, c in enumerate(cols):
        if i == bestIG:
            bestColumn = c
            newNode = treeNode(c.name)
            loweredColumns = cols.copy()
            del loweredColumns[i]
            break

    zData = []
    oData = []
    tData = []

    for d in datas:
        if d[bestColumn.column] == 0:
            zData.append(d)

    n = checkLeaf(loweredColumns, zData)
    if n != None:
        newZero = treeNode("end")
        newZero.classification = n
        newNode.z = newZero
    else:
        newNode.z = treeMaker(loweredColumns, zData)


    for d in datas:
        if d[bestColumn.column] == 1:
            oData.append(d)

    m = checkLeaf(loweredColumns, oData)
    if m != None:
        newOne = treeNode("end")
        newOne.classification = m
        newNode.o = newOne
    else:
        newNode.o = treeMaker(loweredColumns, oData)


    for d in datas:
        if d[bestColumn.column] == 2:
            tData.append(d)

    o = checkLeaf(loweredColumns, tData)
    if o != None:
        newTwo = treeNode("end")
        newTwo.classification = o
        newNode.t = newTwo
    else:
        newNode.t = treeMaker(loweredColumns, tData)


    return newNode


if len(sys.argv) != 3:
    print("Error: requires exactly two arguments: first the training data, the second the test data")
    sys.exit(1)

numColumns = 0
columns = []
trainDataArray = []

with open(sys.argv[1], 'r') as trainData:
    extractTrainData = trainData.readlines()
    classes = extractTrainData[0].split()
    for x in classes[:-1]:
        v = variable(x, numColumns)
        columns.append(v)
        numColumns+=1 
    for indvLine in extractTrainData[1:]:
        splitLine = indvLine.split()
        intArray = [int(numString) for numString in splitLine]
        trainDataArray.append(intArray)

global allData
allData = trainDataArray

t = treeMaker(columns, trainDataArray)
t.printTree("")


trainData.close()
