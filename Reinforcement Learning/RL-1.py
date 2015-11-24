'''
@authors: Akash Gopal
@date: 11/22/2015
'''

import sys
import csv
from math import *

# Grid Dimensions
rowSize = 5
colSize = 4

wall = [(1,1), (1,3)] # Wall position in the grid
gamma = 0.9 # Discount Factor
threshold = 0.001 # Threshold Value 
alpha = 0.1 # Learning Rate
listOfActions = [] # Dictionary which contains actions with their probabbilities
rewardZeroFlag = False # For re-running code with reward set as 0

class actions:
	def __init__(self, action, effects):
		self.action = action
		self.listOfEffects = effects 

def start():	
	global listOfActions
	global rowSize
	global colSize
	global alpha
	listOfActions = []
	listOfActions.append(actions("up", {"up":0.8, "left":0.2}))
	listOfActions.append(actions("down", {"down":1.0}))
	listOfActions.append(actions("left", {"left":1.0}))
	listOfActions.append(actions("right", {"right":0.8, "down":0.2}))

	valueMatrix=[[0 for b in range(colSize)] for a in range(rowSize)]
	
	count = 0 # Counting the number of iterations it takes for values to converge
	while True:
		count+=1		
		tempValueMatrix =[[0 for b in range(colSize)] for a in range(rowSize)]
		for i in range(rowSize): # Creating a copy of the valueMatrix
			for j in range(colSize):			
				tempValueMatrix[i][j] = valueMatrix[i][j]

		for i in range(rowSize):
			for j in range(colSize):
				if (i,j) in wall:
					continue
				Max = -1*sys.maxsize

				for a in listOfActions: # Take a particuler action
					if rewardZeroFlag == True:
					 	reward = 0
					else:
						reward = -1
					if (i,j)  == (3,1):
						reward = -50
					elif (i,j) == (4,3):
						reward = 10
					curMax = -1*sys.maxsize

					for effect in a.listOfEffects.keys(): # For a particular action, go through all possible actions
						inew, jnew = performMove(effect, i, j)	# Obtain the new co-ordinates for the chosen action
						if wallBlocked(inew,jnew):
							continue					
						if (validState(inew, jnew)): # Get value for going to the next state
							curMax = a.listOfEffects[effect] * tempValueMatrix[inew][jnew]
						else:
							curMax = a.listOfEffects[effect] * tempValueMatrix[i][j]
						if Max < curMax:
							Max = curMax
					currentValue = reward + gamma*Max
					# Update the value for current state
					valueMatrix[i][j] = alpha * currentValue + (1 - alpha) * valueMatrix[i][j]

		flag = True
		for i in range(rowSize):
			for j in range(colSize): # check whether values for all the states differ by some state
				if fabs(tempValueMatrix[i][j]-valueMatrix[i][j]) > threshold:
					flag = False
		if(flag==True): # if yes, then stop.
			break
	printValueMatrix(valueMatrix)
	print
	print "Total Number of iterations run ", count																

def performMove(a,i,j):
	''' Returns new co-ordinates for action '''
	if a == "up":
		return (i+1, j)
	if a == "down":
		return (i-1, j)
	if a == "left":
		return (i, j+1)
	if a == "right":
		return (i, j-1)

def wallBlocked(i,j):
	''' Returns whether co-ordinates are wall co-ordinates or not '''
	if (i,j) in wall:
		return True
	return False

def validState(i,j):
	''' Returns whether co-ordinates are valid co-ordinates or not '''
	if i < 0 or i >=rowSize:
		return False
	elif j < 0 or j >= colSize:
		return False
	else:
		return True

def printValueMatrix(v):
	''' Prints Value Matrix '''
	width = 8	
	print
	if rewardZeroFlag == True:
		print "\t\t\t*****************************"
		print "\t\t\tVALUE MATRIX WITH REWARD = 0:"
		print "\t\t\t*****************************"
	else:
		print "\t\t\t******************************"
		print "\t\t\tVALUE MATRIX WITH REWARD = -1:"
		print "\t\t\t******************************"
	print
	rowString = " " * 21 * colSize
	for i in range(rowSize-1,-1,-1):
		print "-"*(len(str(rowString)))
		rowString = ""
		for j in range(0,colSize):
			string = str(float("{0:.6f}".format(v[i][j])))
			spaces = " " *(14-len(string))
			rowString+= (" "* 6)+str(string)+ spaces + "|" 
			#rowString+=str(string) + "|"
		print rowString
	print "-"*(len(str(rowString)))

def main():
	global rewardZeroFlag
	start()
	print
	rewardZeroFlag = True
	start()
	print 
	print 

''' Start of the program '''
if __name__ == "__main__" : main()	
