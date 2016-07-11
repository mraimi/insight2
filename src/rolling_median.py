import sys
import json
from datetime import datetime
from collections import defaultdict

# Checks if the new record can be inserted without pruning or reordering
def windowCheck(newDate, window):
	oldest = window[0]
	if ((newDate - oldest).total_seconds < 60):
		return True
	
	return False

# Inserts an out of order record
def insertToWindow(record, window):
	for i in xrange(0,len(window)):
		if (record[2]-window[i][3].total_seconds() <= 0):
			window.insert(i)

def insertKey(key, degKeys, degCounts):
	if (not len(degKeys)):
		degKeys.append(key)

	if key in degCounts:
		return

	for i in xrange(0,len(degKeys)):
		if (degKeys[i] >= key):
			degKeys.insert(i,key)

def addEdge(adjList, target, actor):
	adjList[target][0] += 1
	adjList[target][1].add(actor)
	adjList[actor][0] += 1
	adjList[actor][1].add(target)


# Updates degree keys and counts when some number of records
# must be pruned from the window
def removeUpdate(pruned,adjList,degKeys,degCounts):
	for record in pruned:
		target = record[0]
		action = record[1]
		currDeg = adjList[target][0]

		for person in (target, actor):
			if (degCounts[adjList[person][0]] == 1):
				removeKey(adjList[person][0], degKeys)
			adjList[target][0] = currDeg - 1 if (currDeg > 1) else 0



# Searches for the first record that doesn't violate the 60 second window constraint
# and returns that index
def pruneIdx(window, newDate):
	for i in xrange(0,len(window)):
		if ((newDate - window[i]).total_seconds < 60):
			return i


# Updates degree keys and counts when inserting out of order records
# in the window
def updateForInsert(adjList, target, actor, degCounts, degKeys):
	for person in (target,actor):
		d = adjList[person][0]
		if (d-1 > 0):
			if (degCounts[d-1] == 1):
				try:
					degKeys.remove(d-1)
				except:
					print "There was an error removing a key (%d) that doesn't exist" % d-1
		
			degCounts[d-1] -= 1
		degCounts[d] += 1
		if (d not in degKeys):
			insertKey(d, degKeys, degCounts)



def getMedian(totalDegrees, degCounts, degKeys):
	print "total degrees %d" % totalDegrees
	for key in degCounts:
		print "%d:%d" % (key,degCounts[key])
	print degKeys
	isEven = totalDegrees%2 == 0
	remaining = totalDegrees/2 - 1
	for key in degKeys:
		if (remaining - degCounts[key] <= 0):
			return key
		else:
			remaining -= degCounts[key]



def new(date, window):
	if (not len(window)):
		return True

	newest = window[len(window)-1]
	# new data is newer than the newest in the window
	if ((newDate - newest).total_seconds > 0):
		return True
	
	return False

def old(date, window):
	oldest = window[0]
	# new data is newer than the newest in the window
	if ((newDate - oldest).total_seconds < 0):
		return True
	
	return False


data = open('../data-gen/venmo-trans.txt', 'r')
adjList = defaultdict(lambda: [0, set()])
window = []
degKeys = []
degCounts = defaultdict(int)
totalDegrees = 0


# 2016-03-28T23:23:12Z
for line in data:
	record = json.loads(line.strip())
	target, actor, date = record['target'], record['actor'], datetime.strptime(record['created_time'], '%Y-%m-%dT%H:%M:%SZ')
	
	
	# Record is new
	if (new(date, window)):
		print 'new!'
		for person in (target,actor):
			if (person not in adjList):
				totalDegrees += 1
		idx = pruneIdx(window,date)
		removeUpdate(window[:idx],adjList,degKeys,degCounts)
		window = window[idx:]
		window.append((target,actor,date))
		addEdge(adjList, target, actor)
		updateForInsert(adjList, target, actor, degCounts, degKeys)
	# Record is out of order
	else:
		if(old(date, window)):
			continue
		# Record must be inserted somewhere within the window
		for person in (target,actor):
			if (person not in adjList):
				totalDegrees += 1
		addEdge(adjList, target, actor)
		updateForInsert(adjList, target, actor, degCounts, degKeys)
		insertToWindow((target,actor,date))



	print getMedian(totalDegrees, degCounts, degKeys)
	print window
	sys.exit()

data.close()
log.close()

# date1 = datetime.strptime('2016-03-28T23:23:19Z','%Y-%m-%dT%H:%M:%SZ')
# date2 = datetime.strptime('2016-03-28T23:23:12Z','%Y-%m-%dT%H:%M:%SZ')
# print (date1-date2).total_seconds()
