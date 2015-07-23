import sys

##Jonathan Kalechstain solution to the problem of assigning similar duties to driver.
##Written for Optibus second interview.


##Munkers is the library that solves the Hungarian algorithm. It was taken from the following
##Link : https://pypi.python.org/pypi/munkres/
from munkres import Munkres, make_cost_matrix

##*************************************************************************************************
#Created a matrix Mnxn filled with zeroes

def createMatrix(n):
    start = []
    for i in range(n):
        start.append([0]*n)
    return start

##*************************************************************************************************

#This function calculates the similarity, between two duties D1, D2

def calcSimilarity (D1, D2):
    D1set = set(D1)
    D2set = set(D2)
    #Compute the intersection of D1, D2 and get the length of it converted to a float.
    nominator = float(len(D1set.intersection(D2set)))
    #Compute the union of D1, D2 and get the length of it.
    dominator = len(D1set.union(D2set))
    return nominator / dominator

##*************************************************************************************************

##Given two days of duties, assign for every driver Pi the duty Di the first day, and then finds
##The best match for the second day (in means of maximum sum)

def assignDuties(dayA, dayB):
    if len(dayA) != len(dayB):
        print "Illegal!! number of duties should be equal every day"
        exit(1)
    matrix = createMatrix(len(dayA))
    ##Fill the matrix with the similarities
    for i in range(len(dayA)):
        for j in range(len(dayA)):
            matrix[i][j] = calcSimilarity(dayA[i], dayB[j])
    ##The following line is called to make sure we find the maximum sum and not the minimum
    ##Note that since all similarities are in [0,1] 2 is bigger than all.
    cost_matrix = make_cost_matrix(matrix, lambda cost: 2 - cost)
    m = Munkres()
    ##Indexes will contain the assignment
    indexes = m.compute(cost_matrix)
    res = []
    for row, column in indexes:
        res.append(("Driver "+str(row + 1) ,("Day 1 duty: "+str(row + 1),"Day 2 duty: "+str(column + 1))))
    return res
    
##*************************************************************************************************


def printList(l):
    for x in l:
        print x
        print

def main(argv):


    #Sanity test, only one matching
    print "Test 1"
    D1A = [("line 1", "9:00-10:00")]
    dayA = [D1A]
    D1B = [("line 1", "9:10-10:00")]
    dayB = [D1B] 
    res = assignDuties(dayA, dayB)
    printList(res)


    ## Checks to see that although D1A contains D1B, we still prefer to match it with D2B as their alignment yields 0.75 and D2A prefers D1B
    ## Because that while the intersection size of it with both D1B and D2B is identical, there are more objects in D2B, which yields the difference.
    print "Test 2"
    D1A = [("line 1", "9:00-10:00"), ("line 2", "10:15-11:00"), ("line 2", "11:30-12:15")]
    D2A = [("line 1" , "9:00-10:00"), ("line 5", "10:30-12:40")]
    D3A = [("line 1", "9:00-10:00"), ("line 6", "11:30-12:30")]
    dayA = [D1A,D2A,D3A]
    D1B = [("line 1", "9:00-10:00"), ("line 2", "10:15-11:00")]
    D2B = [("line 1", "9:00-10:00"), ("line 2", "10:15-11:00"), ("line 2", "11:30-12:15"), ("line 8", "12:20:13:20")]
    D3B = [("line 1", "9:15-10:00"), ("line 6", "11:30-12:30")]
    dayB = [D1B,D2B,D3B]
    res = assignDuties(dayA, dayB)
    printList(res)
    
    # While D2A would prefer to have D1B, because 1 + 0.25 > 0.333... + 0.5 he would not get his first preference
    print "Test 3"
    D1A = [2]
    D2A = [1, 2]
    dayA = [D1A, D2A]
    D1B = [2]
    D2B = [2, 3, 4]
    dayB = [D1B,D2B]
    res = assignDuties(dayA, dayB)
    printList(res)

    # Just another example to check that it's working.
    print "Test 4"
    D1A = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    D2A = [1, 2, 3, 4, 5, 13]
    D3A = [3, 4 ,5 ,6]
    dayA = [D1A,D2A,D3A]
    D1B = [1, 2, 3, 5, 10]
    D2B = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    D3B = [2, 3, 4, 5]
    dayB = [D1B,D2B,D3B]
    res = assignDuties(dayA, dayB)
    printList(res)
    



if __name__ == "__main__":
   main(sys.argv[1:]) 
