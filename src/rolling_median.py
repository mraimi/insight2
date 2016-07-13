import sys
import json
from datetime import datetime
from collections import defaultdict

def getSeconds(date):
    return str(int((date-datetime.datetime(1970,1,1)).total_seconds()))

def getEdgeCount(edgeCounts, target, actor):
    if tuple(sorted((target,actor))) not in edgeCounts:

        return 0

    return edgeCounts[tuple(sorted((target,actor)))]

# Checks if the new record can be inserted without pruning or reordering
def windowCheck(newDate, window):
    oldest = window[0]
    if (newDate - oldest).total_seconds() < 60:
        return True

    return False

# Inserts an out of order record
def insertToWindow(record, window):
    for i in xrange(0,len(window)):
        if (record[2]-window[i][2]).total_seconds() <= 0:
            window.insert(i, record)

def insertKey(key, degKeys):
    if key in degKeys:
        return

    for i in xrange(0,len(degKeys)):
        if degKeys[i] > key:
            degKeys.insert(i,key)

            return
    degKeys.append(key)

    return


def addEdge(adjList, target, actor, date, totalNodes, edgeCounts):
    # target = target + getSeconds()
    if getEdgeCount(edgeCounts,target,actor) == 0:
        if target not in adjList:
            totalNodes += 1

        adjList[target][0] += 1
        adjList[target][1].add(actor)

        if actor not in adjList:
            totalNodes += 1

        adjList[actor][0] += 1
        adjList[actor][1].add(target)

    edgeCounts[tuple(sorted((target,actor)))] += 1

    return totalNodes


# Updates degree keys and counts when some number of records
# must be pruned from the window. Happens BEFORE new edge added
def removeUpdate(toPrune,adjList,degKeys,degCounts,totalNodes, edgeCounts):
    for record in toPrune:
        target = record[0]
        actor = record[1]
        edgeCt = getEdgeCount(edgeCounts,target,actor)
        if edgeCt == 0:
            return totalNodes
            # sys.exit('Graph is inconsistent. Edge count says this edge should not exist')

        if  edgeCt > 0 and edgeCt == 1:
            people = (target, actor)
            for i in xrange(0, len(people)):
                person = people[i]
                opp = people[int(not i)]
                currDeg = adjList[person][0]

                # delete entries from degree keys and counts
                if degCounts[currDeg] == 1:
                    degKeys.remove(currDeg)
                    degCounts.pop(currDeg)
                else:
                    degCounts[currDeg] -= 1
                    insertKey(currDeg, degKeys)
                if currDeg - 1:
                    degCounts[currDeg - 1] += 1
                    insertKey(currDeg - 1, degKeys)

                if currDeg == 1:
                    totalNodes -= 1
                    adjList.pop(person)
                else:
                    adjList[person][0] = currDeg - 1
                    insertKey(currDeg - 1, degKeys)
                    adjList[person][1].remove(opp)
            edgeCounts.pop(tuple(sorted((target,actor))))
        else:
            edgeCounts[tuple(sorted((target,actor)))] -= 1

    return totalNodes



# Searches for the first record that doesn't violate the 60 second window constraint
# and returns that index
def pruneIdx(window, newDate):
    for i in xrange(0,len(window)):
        if (newDate - window[i][2]).total_seconds() < 60:
            return i

    return len(window)


# Updates degree keys and counts AFTER adding the new edge
# TODO: update to use edgeCounts? Fix degCounts - they're going negative
def updateKeysCounts(adjList, target, actor, degCounts, degKeys, edgeCounts, exists):
    if not exists:
        for person in (target,actor):
            d = adjList[person][0]
            if d-1 in degCounts and d-1 > 0 and degCounts[d-1] > 0:
                if degCounts[d-1] == 1:
                    try:
                        degKeys.remove(d-1)
                        degCounts.pop(d-1)
                    except:
                        print "There was an error removing a key (%d) that doesn't exist" % d-1
                else:
                    degCounts[d-1] -= 1
            if d > 0:
                degCounts[d] += 1
            insertKey(d, degKeys)



def getMedian(totalNodes, degCounts, degKeys):
    # for key in degCounts:
        # print "%d:%d" % (key,degCounts[key])
    isEven = totalNodes%2 == 0
    remaining = totalNodes/2
    for i in xrange(0,len(degKeys)):
        key = degKeys[i]
        diff = remaining - degCounts[key]
        if diff <= 0:
            if len(degKeys) == 1:
                return key
            else:
                return (key+degKeys[i+1])/2.0 if (isEven and diff == 0) else key
        else:
            remaining -= degCounts[key]



def new(newDate, window):
    if (not len(window)):
        return True

    newest = window[len(window)-1][2]
    # new data is newer than the newest in the window
    if ((newDate - newest).total_seconds() >= 0):
        return True

    return False

def old(newDate, window):
    oldest = window[0][2]
    # new data is newer than the newest in the window
    if ((newDate - oldest).total_seconds() < 0):
        return True

    return False


# data = open('../data-gen/requiresPruning.txt', 'r')
data = open('../data-gen/venmo-trans.txt', 'r')
adjList = defaultdict(lambda: [0, set()])
window = []
degKeys = []
degCounts = defaultdict(int)
edgeCounts = defaultdict(int)
totalNodes = 0
ct = 0
for line in data:
    ct += 1
    record = json.loads(line.strip())
    if len(record) != 3:
        continue
    target, actor, date = record['target'], record['actor'], datetime.strptime(record['created_time'], '%Y-%m-%dT%H:%M:%SZ')


    # Record is new
    if (new(date, window)):
        exists = tuple(sorted((target,actor))) in edgeCounts
        idx = pruneIdx(window,date)
        totalNodes = removeUpdate(window[:idx],adjList,degKeys,degCounts,totalNodes,edgeCounts)
        window = window[idx:]
        window.append((target,actor,date))
        totalNodes = addEdge(adjList, target, actor, date, totalNodes, edgeCounts)
        updateKeysCounts(adjList, target, actor, degCounts, degKeys, edgeCounts, exists)
    # Record is out of order
    else:
        if(old(date, window)):
            print "median: " + str(getMedian(totalNodes, degCounts, degKeys))
            continue
        exists = tuple(sorted((target, actor))) in edgeCounts
        totalNodes = addEdge(adjList, target, actor, date, totalNodes, edgeCounts)
        updateKeysCounts(adjList, target, actor, degCounts, degKeys, edgeCounts, exists)
        insertToWindow((target,actor,date), window)


    print str(getMedian(totalNodes, degCounts, degKeys))

    # if (ct == 5):
    # 	break

data.close()
