"""
Authors: Karthik Handady & Andrew Gordan
Purpose: The purpose of this program is to cluster sequences from a fasta file into a phylogenetic tree.

Usage:  To use the program the command line argument is:
        HW_4.py -f filename.fasta -g gap_penalty -s scoring matrix
        -f is the argument where the fasta file location and name is given
        -g is the argument where the user inputs the gap-penalty score
        -s is the argument where the scoring matrix location is given

References: https://docs.python.org/2/library/getopt.html (Option parsing library)

Algorithm:
1.Get Command line arguments
2.Open fasta file and extract sequences into array
3.

#Detailed algorithm description
"""


import sys
import getopt


#Guide Tree Class
class Guide_Tree_Node:

    leftchild = None
    rightchild = None
    data = ""
    distance = 0

    def __init__(self, leftchild, rightchild, data, distance):
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.data = data
        self.distance = distance


#Main function simply calls all the functions in order and passes the necessary parameters
def main():
    fastafile , matrixfile, gap_penalty = parsecommand()
    arrayofsequences, scorematrix = readfiles(fastafile, matrixfile)
    alignments = globalalignment(arrayofsequences, scorematrix, gap_penalty)
    printalignment(alignments)


#The parsecommand function takes in the commandline arguments using getopt and checks
# that the arguments are entered and alerts user if there is anything wrong with the
# commandline arguments. If no errors it returns the fasta and scoring matrix file names and the gap_penalty

def parsecommand():
    #Define variables
    fastafile = ''
    matrixfile = ''
    gap_penalty_set = 0
    #get command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:g:s')
    except getopt.GetoptError as err:
        print(err)
        print('Command line arguments were incorrect. Please rerun with correct arguments.')
        sys.exit(1)

    #put the arguments into the right variables
    for opt , arg in opts:
        if opt == '-f':
            fastafile = arg
        if opt == '-l':
            matrixfile = arg
        if opt == '-g':
            gap_penalty = arg
            gap_penalty_set = 1

    # Check that mandatory arguments were entered
    if fastafile == '' or matrixfile == '' or gap_penalty_set == 0:
        print("Arguments not entered. Please run again with correct arguments.")
        sys.exit(1)

    #Just for checking
    #print('Fasta File: ' + fastafile)
    #print('Matrix File: ' + matrixfile)
    #print('Gap_penalty: ' + gap_penalty)
    return fastafile, matrixfile, gap_penalty


#The readfiles function reads the fasta file and extracts the sequences and places them in
#an array and reads the scoring matrix file and extracts the scores into a matrix.
#The function then returns the sequence array and scoring matrix to main where it can be further processed.

def readfiles(fastafile, matrixfile):
    arrayofsequences = []

    #Temp scoring matrix
    scorematrix = [[3,-1,-1,-1,-1],[-1,3,-1,-1,-1],[-1,-1,3,-1,-1],[-1,-1,-1,3,-1],[-1,-1,-1,-1,0]]
    sequence = ''
    counter = 0
    fp = open(fastafile,"r")  #open file

    #Read in each sequence in the fasta file
    for line in fp:
        if(line[0] != '>'):
            sequence += line
        else:
            arrayofsequences.append(sequence.strip('\n'))
            counter += 1
            sequence = ''

    #Put in the last sequence into the array
    arrayofsequences.append(sequence.strip('\n'))
    counter += 1
    #Remove the empty string in the beginning of the array
    arrayofsequences = arrayofsequences[1:counter]

    return arrayofsequences, scorematrix


#The globalalignment function runs if the user did not enter an argument and is run by default.
#The function takes in the array of sequences and pairs them off and calls on makeglobalmatrix() to initialize and scoreglobalalignment() to score the matrix
#The function then calls getglobalalignment() to generate the aligned sequences
#The function then places the aligned sequences and score into an array and passes it back to main

def globalalignment(arrayofsequences, scoringmatrix, gap_penalty):
    alignmentscores = []
    for i in range(0,len(arrayofsequences)-1):
        for j in range(1, len(arrayofsequences)):
            alignmentgrid = makeglobalmatrix(arrayofsequences[i],arrayofsequences[i+1])
            score = scoreglobalalignment(alignmentgrid,arrayofsequences[i],arrayofsequences[i+1], scoringmatrix, gap_penalty)
            alignmentscores.append(score)

    return alignmentscores

#The makeglobalmatrix function generates the scoring matrix by setting all values to zero and generates the arrow matrix
# by setting all values to empty string. The program then puts the null string penalty into the top row and leftmost column
# and then returns the scoring and arrow matrix
def makeglobalmatrix(sequence1,sequence2):
    alignmentgrid = [[0 for x in range(len(sequence1)+1)] for x in range(len(sequence2)+1)]

    #fill in top row for null string
    for x in range(len(sequence1)+1):
        alignmentgrid[0][x] = x*1
    #fill in leftmost column for null string
    for x in range(len(sequence2)+1):
        alignmentgrid[x][0] = x*1

    return alignmentgrid


#The scoreglobalalignment function takes the initialized scoring and arrow matrix and starts generating the values
#that go in them using the scoring guide which is defined by the scoring matrix and gap_penalty
#The arrow matrix remembers where the values came from and is passed back along with the score at the function end.
def scoreglobalalignment(alignmentgrid, sequence1, sequence2, scoringmatrix, gap_penalty):

    for x in range(1,len(sequence2)+1,1):
        for y in range(1,len(sequence1)+1,1):

            #Get mismatch score from scoring matrix
            if(sequence2[x-1] != sequence1[y-1]):
               

            up = alignmentgrid[x][y-1] - gap_penalty
            left = alignmentgrid[x-1][y] - gap_penalty
            diagonal = alignmentgrid[x-1][y-1] + mismatch


    #Score is bottom right corner of grid
    score = alignmentgrid[len(sequence2)][len(sequence1)]

    return score


main()