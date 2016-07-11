import sys
import json
from datetime import datetime
from collections import defaultdict

# Checks if the new record can be inserted without pruning or reordering
def windowCheck(newDate, window):
	oldest = window[0]
	if ((newDate - oldest).total_seconds() < 60):
		return True
	
	return False

# Inserts an out of order record
def insertToWindow(record, window):
	for i in xrange(0,len(window)):
		if ((record[2]-window[i][2]).total_seconds() <= 0):
			window.insert(i, record)

def insertKey(key, degKeys, degCounts):
	# print 'key to add: ' + str(key)

	if key in degKeys:
		return

	for i in xrange(0,len(degKeys)):
		if (degKeys[i] > key):
			degKeys.insert(i,key)

			return
	degKeys.append(key)

	return


def addEdge(adjList, target, actor, totalNodes):
	if (target not in adjList):
		totalNodes += 1

	adjList[target][0] += 1
	adjList[target][1].add(actor)

	if (actor not in adjList):
		totalNodes += 1
	adjList[actor][0] += 1
	adjList[actor][1].add(target)

	return totalNodes


# Updates degree keys and counts when some number of records
# must be pruned from the window
def removeUpdate(pruned,adjList,degKeys,degCounts,totalNodes):
	
	print "prune: " + str(pruned)
	for record in pruned:
		target = record[0]
		actor = record[1]

		
		people = (target, actor)
		for i in xrange(0, len(people)):
			# print adjList[adjList.keys()[0]]
			# print adjList[adjList.keys()[1]]
			person = people[i] 
			opp = people[int(not i)]
			currDeg = adjList[person][0]
			if (currDeg == 1):
				totalNodes -= 1
			print 'updated total:' + str(totalNodes)
			if (degCounts[currDeg] == 1):
				degKeys.remove(currDeg)
				degCounts.pop(currDeg)
			else:
				degCounts[currDeg] -= 1
			if (currDeg == 1):
				adjList.pop(person)
			else:
				adjList[person][0] = currDeg - 1
				adjList[person][1].remove(opp)
			print adjList[target][1]
			

	return totalNodes



# Searches for the first record that doesn't violate the 60 second window constraint
# and returns that index
def pruneIdx(window, newDate):
	for i in xrange(0,len(window)):
		if ((newDate - window[i][2]).total_seconds() < 60):
			return i

	return len(window)


# Updates degree keys and counts when inserting out of order records
# in the window
def updateForInsert(adjList, target, actor, degCounts, degKeys):
	for person in (target,actor):
		d = adjList[person][0]
		print person + " deg: %d" % d
		if (d-1 > 0 and degCounts[d-1] > 0):
			if (degCounts[d-1] == 1):
				try:
					degKeys.remove(d-1)
					degCounts.pop(d-1)
				except:
					print "There was an error removing a key (%d) that doesn't exist" % d-1
			else:
				degCounts[d-1] -= 1
		if (d > 0):
			degCounts[d] += 1
		# print 'degCounts: ' + str(degCounts.keys())
		insertKey(d, degKeys, degCounts)



def getMedian(totalNodes, degCounts, degKeys):
	for key in degCounts:
		print "%d:%d" % (key,degCounts[key])
	print "keys: "  + str(degKeys)
	isEven = totalNodes%2 == 0
	remaining = totalNodes/2
	for i in xrange(0,len(degKeys)):
		key = degKeys[i]
		diff = remaining - degCounts[key]
		if (diff <= 0):
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


data = open('../data-gen/requiresInsert.txt', 'r')
adjList = defaultdict(lambda: [0, set()])
window = []
degKeys = []
degCounts = defaultdict(int)
totalNodes = 0

ct = 0
# 2016-03-28T23:23:12Z
for line in data:
	ct += 1

	record = json.loads(line.strip())
	target, actor, date = record['target'], record['actor'], datetime.strptime(record['created_time'], '%Y-%m-%dT%H:%M:%SZ')
	
	
	# Record is new
	if (new(date, window)):
		idx = pruneIdx(window,date)
		print "idx: %d" % idx
		print "total nodes before: %d" % totalNodes
		totalNodes = removeUpdate(window[:idx],adjList,degKeys,degCounts,totalNodes)
		print "total nodes after %d" % totalNodes

		window = window[idx:]
		window.append((target,actor,date))
		totalNodes = addEdge(adjList, target, actor, totalNodes)
		updateForInsert(adjList, target, actor, degCounts, degKeys)
	# Record is out of order
	else:
		print 'out of order'
		if(old(date, window)):
			continue
		totalNodes = addEdge(adjList, target, actor, totalNodes)
		updateForInsert(adjList, target, actor, degCounts, degKeys)
		insertToWindow((target,actor,date), window)


	print "median: " + str(getMedian(totalNodes, degCounts, degKeys)) + "\n"
	print "total nodes: " + str(totalNodes)
	# print window
	# print degKeys

	if (ct == 5):
		break

data.close()

# date1 = datetime.strptime('2016-03-28T23:23:19Z','%Y-%m-%dT%H:%M:%SZ')
# date2 = datetime.strptime('2016-03-28T23:23:12Z','%Y-%m-%dT%H:%M:%SZ')
# print (date1-date2).total_seconds()
