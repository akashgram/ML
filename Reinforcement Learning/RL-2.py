'''
@author: Akash Gopal
@date: 11/22/2015
'''

import sys
import csv
from math import *
import random

# Grid Dimensions
rowSize = 5
colSize = 4

wall = [(3,1), (3,3)] # Wall position in the grid
epsilon = 0.5 # Exploit Vs Explore 
gamma = 0.9 # Discount Factor
alpha = 0.1 # Learning Rate
rewardZeroFlag = False # For re-running code with reward set as 0
def start():	
	global rowSize
	global colSize
	global epsilon
	global gamma
	global alpha
	acts = ["up", "down", "left", "right"] # All the actions possible
	# qValue is a grid of three dimensions where each grid holds values for the 4 possible actions
	qValue = [[{"right":0, "left":0, "up":0, "down":0} for x in range(colSize)] for y in range(rowSize)]
	state = (rowSize-1, 0) # contains the grid values
	countEpisodes=0 # counting the number of episodes
	epsilon = 0.5 # resetting epsilon for re-running code with reward set as 0
	while True:
		flag = True # flag to restart epsiode 
		while flag==True:
			if state==(0, colSize-1): 
				flag = False

			action=""
			maxAction = ""
			maxValue = -1*sys.maxsize
			for act in acts:
				if qValue[state[0]][state[1]][act] > maxValue: # Finding the maximum value and action in current state
					maxValue = qValue[state[0]][state[1]][act]
					maxAction = act	

			# Choosing between exploitation or exploration
			epsilonRound = round(epsilon*1000)	
			val = random.choice(range(int(epsilonRound)+1))
			
			# Explore
			if val < float(epsilonRound/2): 
				val = random.choice(range(3)) 
				i = 0
				for a in acts:
					if a == maxAction:									
						continue
					elif i==val: 
						action = a
						break
					i+=1
			else: # Exploit
				action = maxAction
			
			# Obtain the new state for the chosen action
			newI, newJ, reward = performMove(state[0], state[1], action)

			maxValNext = -1*sys.maxsize
			for a in acts:
				if qValue[newI][newJ][a] > maxValNext: # Finding the maximum value for next state
					maxValNext = qValue[newI][newJ][a]

			# Update Q-Value for current state
			qValue[state[0]][state[1]][action] = (1-alpha)*(qValue[state[0]][state[1]][action]) + alpha*(reward + gamma*maxValNext)
			state = (newI, newJ) # Update the state 
		
		state = (rowSize-1, 0) # Reset the start position for next episode
		countEpisodes+=1	
		if countEpisodes%10 == 0: # Decreasing the exploration after every 10 iterations
			epsilon = epsilon/(1+epsilon)
		if countEpisodes>100000:
			break

	printQValue(qValue)

def reward(i, j):
	''' Returns the reward for a particular state '''
	if (i,j)  == (1,1):
		return -50 
	elif (i,j) == (0,3):
		return 10 
	if rewardZeroFlag == True:
		return 0
	return -1

def performMove(i, j, action): 
	''' Returns new co-ordinates for action '''
	global rowSize
	global colSize
	tempI=i
	tempJ=j
	act = action  

	if act == "up":
		if i-1 >=0:
			tempI = i-1
						
	elif act == "down":
		if(i+1) < rowSize:
			tempI = i+1
						
	elif act == "left":
		if j-1 >=0:
			tempJ = j-1
	elif act == "right":
		if j+1 < colSize:
			tempJ = j+1

	if (tempI,tempJ) in wall:
		return (i, j, reward(i,j))	

	return (tempI, tempJ, reward(tempI,tempJ))	

def printString(string, width):
	''' Returns value with appropriate spaces '''
	temp=""	
	string = float("{0:.2f}".format(string))
	spaces = width - len(str(string))
	for i in range(spaces/2):
		temp+=" "
	temp+= str(string)
	for i in range(spaces-spaces/2):
		temp+=" "
	return temp
	
def printQValue(qValue):
	''' Prints the Q-value '''
	global rowSize
	global colSize
	global rewardZeroFlag
	width = 8
	print 
	if rewardZeroFlag == True:
		print "\t\t\t\t\t*********************"
		print "\t\t\t\t\tGRID WITH REWARD = 0:"
		print "\t\t\t\t\t*********************"
	else:
		print "\t\t\t\t\t**********************"
		print "\t\t\t\t\tGRID WITH REWARD = -1:"
		print "\t\t\t\t\t**********************"
	print 
	for i in range(rowSize):
		print "-"*(width*3+1)*colSize
		temp1 = ""
		temp2 = ""
		temp3 = ""
		spaces = " "*width
		for j in range(colSize):
			temp1 += spaces + printString(qValue[i][j]["up"], width) + spaces + "|"
			
			temp2 += printString(qValue[i][j]["left"], width) + spaces + printString(qValue[i][j]["right"], width) + "|"
			
			temp3 += spaces + printString(qValue[i][j]["down"], width) + spaces + "|"		
		print temp1
		print temp2
		print temp3
	print "-"*(width*3+1)*colSize
	print 	

def main():
	global rewardZeroFlag
	start()
	rewardZeroFlag = True
	start()

''' Start of the program '''
if __name__ == "__main__" : main()
