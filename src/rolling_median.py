import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Checks if the new record can be inserted without pruning or reordering
def windowCheck(date, window):
	return True

# Inserts an out of order record
def insertRecord(record, window):
	return None

# Removes records that violate the 60-second window constraint
# Appends the new record after sufficient pruning
def pruneThenAdd(newRecord, window):
	return None

def getMedian(nums):
	return None

# theory for rolling median found here:
# http://stackoverflow.com/questions/10657503/find-running-median-from-a-stream-of-integers

data = open('../data-gen/venmo-trans.txt', 'r')
adjList = defaultdict(lambda: [0, set()])
window = []


# 2016-03-28T23:23:12Z
for line in data:
	record = json.loads(line.strip())
	target = record['target']
	actor = record['actor']
	date = datetime.strptime(record['created_time'], '%Y-%m-%dT%H:%M:%SZ')
	
	adjList[target][0] += 1
	adjList[target][1].add(actor)
	adjList[actor][0] += 1
	adjList[actor][1].add(target)
	
	if (windowCheck(date, window)):
		window.append((target,actor,date))

	print window
	sys.exit()

# date1 = datetime.strptime(json.loads(data.readline())['created_time'],'%Y-%m-%dT%H:%M:%SZ')
# date2 = datetime.strptime(json.loads(data.readline())['created_time'],'%Y-%m-%dT%H:%M:%SZ')
# print (date1-date2).total_seconds()





