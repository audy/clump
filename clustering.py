#!/usr/local/bin/python

import sys
from Pycluster import *
from pylab import *
from collections import defaultdict

def main():
    """docstring for main"""
    
    filename = sys.argv[1]
    
    # Load tables
    with open(filename) as handle:
        data = load_table(handle)
        
    
    distance_functions = {
        'Pearson Correlation': 'c',
        'Absolute Pearson Correlation': 'a',
        'Uncentered Pearson Correlation': 'u',
        'Absolute uncentered Pearson Correlation': 'x',
        'Spearman\'s Rank Correlation': 's',
        'Kendall\'s T': 'k',
        'Euclidean distance': 'e',
        'City-block distance': 'b',
    }
    
    algorithms = {
        '': '',
    }
    
    # We only want to consider {cases} versus {controls}
    flat_data = {}
    for k in data:
        i = data[k]
        flat_data[k] = [sum(i['cases']), sum(i['controls'])]

    print 'clustering'
    clusterid, error, nfound = kcluster(
                        flat_data.values(),
                        nclusters=2,
                        mask=None,
                        weight=None,
                        transpose=0,
                        npass=1000,
                        method='a',
                        dist='c',
                        initialid=None)
                                    
    # Load clusters into dictionary
    clusters = defaultdict(list)
    for i, j in zip(clusterid, data):
        clusters[i].append(j)

    
    # Print output so that it makes sense
   # print_clusters(clusters)
    print 'plotting'    
    
    # Plot clusters by color
    plot_clusters(clusters, flat_data)
    
    
    
def print_clusters(clusters):
    """ Prints something that makes sense. """
    for i in clusters:
        print '    Cluster %s:' % i
        for j in sorted(clusters[i]):
            print '        %s' % (j)
            
                
def plot_clusters(clusters, flat_data):
    """ plots clustering output """
    
    fig = figure()
    ax1 = fig.add_subplot(111)
    
    colors = ['b', 'y', 'g', 'r', 'c']
    
    vectors = {}
    
    for c in clusters:
        color = colors[c]
        vectors[color] = []
        for g in clusters[c]:
            v = flat_data[g]
            vectors[color].append(v)
            
        plt.scatter([v[0] for v in vectors[color]], 
        [v[1] for v in vectors[color]], s=20, c=color, marker='s')    

    
    show()
    
    
def load_table(handle):
    """ Loads Data Table """
    data = {}
    for line in handle:
        if line.startswith('#'):
            continue
            
        line = line.strip().split(',')
        values = line[:-1]
        gene = line[-1]
        if '#' in gene: continue
        if gene.count(';') != 4: continue
        gene = gene.split(',')[-1]
        data[gene] = { 'cases': [int(i) for i in values[4:]],
                       'controls': [int(i) for i in values[:4]] }
    
    return data
    
if __name__ == '__main__':
    main()