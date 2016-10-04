# Importing the necessary libraries for the program

# Importing numpy to perform matrix multiplications
import numpy as np 

# Importing pandas to read data as a data frame
import pandas as pd 

# Importing math to perform trigonometric operations
import math 

MIN_VALUE = 6.12323400e-17 # Setting the min value 

# Reading the DH parameters of robot as a CSV file
df = pd.read_csv('dh_parameters.csv') 

# Function to make the Transformation Matrix for d,a,alpha and theta
def transformationMatrix(d,a,alpha,theta):
	
	# Converting theta from degrees to radians
	theta = math.radians(theta)

	# Converting alpha from degrees to radians
	alpha = math.radians(alpha)

	# Calculating the first row of matrix
	element_11 = math.cos(theta) \
	if abs(math.cos(theta)) > MIN_VALUE else 0.00

	element_12 = -1*math.sin(theta)*math.cos(alpha)\
	if abs(-1*math.sin(theta)*math.cos(alpha)) > MIN_VALUE else 0.00

	element_13 = math.sin(theta)*math.sin(alpha) \
	if abs(math.sin(theta)*math.sin(alpha)) > MIN_VALUE else 0.00

	element_14 = a*math.cos(theta)
	


	# Calculating the second row of matrix
	element_21 = math.sin(theta) \
	if abs(math.sin(theta)) > MIN_VALUE else 0.00

	element_22 = math.cos(theta)*math.cos(alpha) \
	if abs(math.cos(theta)*math.cos(alpha)) > MIN_VALUE else 0.00

	element_23 = -1*math.cos(theta)*math.sin(alpha) \
	if abs(math.cos(theta)*math.sin(alpha)) > MIN_VALUE else 0.00

	element_24 = a*(math.sin(theta))
	
	

	# Calculating the third row of matrix
	element_31 = 0

	element_32 = math.sin(alpha) \
	if abs(math.sin(alpha)) > MIN_VALUE else 0.00

	element_33 = math.cos(alpha) \
	if abs(math.cos(alpha)) > MIN_VALUE else 0.00

	element_34 = d


	# Calculating the fourth row of matrix
	element_41 = 0

	element_42 = 0

	element_43 = 0

	element_44 = 1

	# Returning the transformation matrix
	return np.matrix([[element_11,element_12,element_13,element_14],
	[element_21,element_22,element_23,element_24],
	[element_31,element_32,element_33,element_34],
	[element_41,element_42,element_43,element_44]])

# Calculating the number of rows in DH Table
number_of_rows, number_of_columns = df.shape

# Setting the Identity matrix as initial Transformation Matrix
T_0n = np.matrix([[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]])

# Iterating through all the rows in the DH Table to obtain pairwise 
# Transformation Matrices
for index,row in df.iterrows():
	print "Printing the Transformation Matrix T_" + str(index) + str((index+1))
	
	temp = transformationMatrix(row['d'],row['a'],row['alpha'],row['theta'])
	print temp 
	
	T_0n = T_0n * temp

print "Printing the Transformation Matrix T_0" + str(number_of_rows)
print T_0n

# Calculating the position vector of the tool tip
position_vector = np.array([[T_0n.item((0,3))],[T_0n.item((1,3))],[T_0n.item((2,3))]])
print "Position Vector of end effector"
print position_vector

# Calculating the rotation matrix of the tool tip
rot_mat = np.matrix([[T_0n.item((0,0)),T_0n.item((0,1)),T_0n.item((0,2))],
	         [T_0n.item((1,0)),T_0n.item((1,1)),T_0n.item((1,2))],
	         [T_0n.item((2,0)),T_0n.item((2,1)),T_0n.item((2,2))]])
print "Rotation Matrix of end effector"
print rot_mat