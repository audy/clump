#!/usr/local/bin/python

import sys
from Pycluster import *
from collections import defaultdict

def main():
    """docstring for main"""
    
    filename = sys.argv[1]
    
    # Load tables
    data = {}
    
    with open(filename) as handle:
        for line in handle:
            if line.startswith('#'):
                continue
                
            line = line.strip().split(',')
            values = line[:-1]
            gene = line[-1]
            if '#' in gene: continue
            if gene.count(';') > 0: continue
            data[gene] = [ int(i) for i in values ]
            
    clusterid, error, nfound = kcluster(data.values(), nclusters=5, mask=None,
        weight=None, transpose=0, npass=10000, method='a', dist='a',
        initialid=None)
        
    # Print output so that it makes sense
    
    clusters = defaultdict(list)
    
    for i, j in zip(clusterid, data):
        clusters[i].append(j)
        
    for i in clusters:
        print 'Cluster %s:' % i
        for j in clusters[i]:
            print '    %s' % (j)
    
    

if __name__ == '__main__':
    main()