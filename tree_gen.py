import sys
from ete3 import Tree
import ete3 #for good error messages
import six.moves.cPickle as pickle

'''
	python 2. 7 program
	input your tree on command line in double quotes!
'''

try:
	newick_trees = sys.argv[1:]
except:
	print "There were errors in parsing the command line!"
	sys.exit(1)

try:
	for tree_string in newick_trees:
		t = Tree(tree_string)
		t.show()
except ete3.parser.newick.NewickError, e:
	print "invalid newick tree:", e
