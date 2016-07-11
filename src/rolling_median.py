import sys
import json
from datetime import datetime
from collections import defaultdict

# Checks if the new record can be inserted without pruning or reordering
def windowCheck(newDate, window):
	oldest = window[0]
	if ((newDate - oldest).total_seconds < 60)
		return True
	
	return False

# Inserts an out of order record
def insertToWindow(record, window):
	return None

def insertKey(key, degKeys):
	for i in xrange(0,len(degKeys)):
		if (degKeys[i] >= key):
			degKeys.insert(key)

def addEdge(adjList, target, actor):
	adjList[target][0] += 1
	adjList[target][1].add(actor)
	adjList[actor][0] += 1
	adjList[actor][1].add(target)

def removeUpdate(pruned,adjList,degKeys,degCounts):
	for record in pruned:
		target = record[0]
		action = record[1]
		currDeg = adjList[target][0]

		for person in (target, actor)
			if (degCounts[adjList[person][0]] == 1):
				removeKey(adjList[person][0], degKeys)
			adjList[target][0] = currDeg - 1 if (currDeg > 1) else 0



# Searches for the first record that doesn't violate the 60 second window constraint
# and returns that index
def pruneIdx(window, newDate):
	for i in xrange(0,len(window)):
		if ((newDate - window[i]).total_seconds < 60):
			return i

def updateOnInsert(adjList, target, actor, degCounts, degKeys):
	#target
	for person in (target,actor):
		d = adjList[person][0]
		if (degCounts[d-1] == 1):
			try:
				degKeys.remove(d-1)
			except:
				print "There was an error removing a key (%d) that doesn't exist" % d-1
		degCounts[d-1] -= 1
		degCounts[d] += 1
		if (d not in degKeys):
			insertKey(d, degKeys)



def getMedian(nums):
	return None

def new(date, window):
	newest = window[len(window)]
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





# theory for rolling median found here:
# http://stackoverflow.com/questions/10657503/find-running-median-from-a-stream-of-integers

data = open('../data-gen/venmo-trans.txt', 'r')
adjList = defaultdict(lambda: [0, set()])
window = []
degKeys = []
degCounts = defaultdict(int)


# 2016-03-28T23:23:12Z
for line in data:
	record = json.loads(line.strip())
	target, actor, date = record['target'], record['actor'], datetime.strptime(record['created_time'], '%Y-%m-%dT%H:%M:%SZ')
	
	# Case where new record can safely be added to the window
	# if (windowCheck(date, window)):
	# 	window.append((target,actor,date))
	# elif ((date - oldDate).total_seconds < 60)
	# 	

	# Record is new
	if (new(date, windows)):
		idx = pruneIdx(window,date)
		removeUpdate(window[:idx],adjList,degKeys,degCounts)
		window = window[idx:]
		window.append((target,actor,date))
	# Record is out of order
	else:
		if(old(date, window)):
			continue
		# Record must be inserted somewhere within the window
		addEdge(adjList, target, actor)
		updateOnInsert(adjList, target, actor, degCounts, degKeys)
		insertToWindow()

	print window
	sys.exit()

data.close()
log.close()

# date1 = datetime.strptime('2016-03-28T23:23:19Z','%Y-%m-%dT%H:%M:%SZ')
# date2 = datetime.strptime('2016-03-28T23:23:12Z','%Y-%m-%dT%H:%M:%SZ')
# print (date1-date2).total_seconds()





