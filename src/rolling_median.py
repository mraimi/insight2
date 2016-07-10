import sys
import json
from datetime import datetime
from collections import defaultdict

# Checks if the new record can be inserted without pruning or reordering
def windowCheck(newDate, window):
	oldest = window[0]
	if ((newDate - oldDate).total_seconds < 60)
		return True
	
	return False

# Inserts an out of order record
def insertRecord(record, window):
	return None

def removeRecord(record, adjList)

def addEdge(adjList, target, actor):
	adjList[target][0] += 1
	adjList[target][1].add(actor)
	adjList[actor][0] += 1
	adjList[actor][1].add(target)

def updatePruned(pruned):
	for rec in pruned:


# Removes records that violate the 60-second window constraint
# Returns the updated window
def pruneIdx(window, newDate):
	for i in xrange(0,len(window)):
		if ((newDate - window[i]).total_seconds < 60):
			return i

def updateKeys():

def updateCounts():
def getMedian(nums):
	return None



# theory for rolling median found here:
# http://stackoverflow.com/questions/10657503/find-running-median-from-a-stream-of-integers

data = open('../data-gen/venmo-trans.txt', 'r')
adjList = defaultdict(lambda: [0, set()])
window = []
degKeys = []
degCounts = {}


# 2016-03-28T23:23:12Z
for line in data:
	record = json.loads(line.strip())
	target, actor, date = record['target'], record['actor'], datetime.strptime(record['created_time'], '%Y-%m-%dT%H:%M:%SZ')
	
	addEdge(adjList, target, actor)
	updateKeys()
	updateCounts()
	
	if (windowCheck(date, window)):
		window.append((target,actor,date))
	else:
		idx = prune(window,date)

	print window
	sys.exit()

# date1 = datetime.strptime('2016-03-28T23:23:19Z','%Y-%m-%dT%H:%M:%SZ')
# date2 = datetime.strptime('2016-03-28T23:23:12Z','%Y-%m-%dT%H:%M:%SZ')
# print (date1-date2).total_seconds()





