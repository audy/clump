#!/usr/local/bin/python

import sys
from pylab import *
import math

def main():
    """ GUTS """
    filename = sys.argv[1]
    
    with open(filename) as handle:
        table = load_table(handle)
    
    # Normalize it 
    table = normalize_table(table)
    
    # First, let's try cases versus controls
    vectors = set()
    for k in table:
        case = sum(i for i in table[k][:4])
        control = sum(i for i in table[k][4:])

        v = Vector(case, control)
        vectors.add(v)
        
    # Plot it!
    plot_table(vectors)

def plot_table(vectors):
    """ Array for Vectors -> Scatter Plot """
    fig = figure()
    ax1 = fig.add_subplot(111)

    plt.scatter([v.x for v in vectors], 
        [v.y for v in vectors], s=20, c='b', marker='s')

    show()
    
    
def normalize_table(table):
    """ Normalizes you a table by dividing each entry in a column
by the sum of that column """

    sums = [0]*len(table.values()[0])
    
    for k in table:
        for i in range(len(table[k])):
            sums[i] += table[k][i]
            
    for k in table:
        for i in range(len(table[k])):
            table[k][i] = table[k][i]/float(sums[i])

    return table
    

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return '|%2ei + %2ej| = %2e' % (self.x, self.y, self.r)

        
class Nector(object):
    """ N dimensional vector """
    def __init__(self, values=[0]):
        self.vs = [ i for i in args ]


def load_table(handle):
    """ Loads baby diet table """
    table = {}
    
    for line in handle:
        line = line.strip()
        if line.count(';') > 1:
            continue
        line = line.split(', ')
        table[line[-1]] = [ int(i) for i in line[:-1] ]
        
    return table
    
if __name__ == '__main__':
    main()