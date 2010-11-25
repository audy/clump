#!/usr/local/bin/python

import sys
from Pycluster import *

def main():
    """docstring for main"""
    
    filename = sys.argv[1]
    
    # Load tables
    data = []
    
    with open(filename) as handle:
        for line in handle:
            if line.startswith('#'):
                continue
                
            line = line.strip().split(',')
            values = line[:-1]
            data.append([ int(i) for i in values])
            
    clusterid, error, nfound = kcluster(data, nclusters=5, mask=None,
        weight=None, transpose=0, npass=1, method='a', dist='k',
        initialid=None)
        
    # An array containing the number of the cluster to which each
    # gene/microarray was assigned.
    
    
    print clusterid, error, nfound
    
    

if __name__ == '__main__':
    main()