#!/usr/local/bin/python

import sys
import Pycluster as pc
from pylab import *
from collections import defaultdict

colors = ['green', 'blue', 'orange', 'cyan',
            'magenta', 'red', 'yellow', 'pink', 'purple']

def main():
    """docstring for main"""
    
    filename = sys.argv[1]
    
    # Load tables
    with open(filename) as handle:
        data, flat_data = load_table(handle)
        
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
    
    nclusters, method, distance = 5, 'a', 'b'
    
    clusters = k_means(flat_data, data, nclusters, method, distance)
    make_plots('k-means: n=%s, m=%s, d=%s' % \
        (nclusters, method, distance), clusters, flat_data)
    
    hierarchical(flat_data, data, nclusters, method, distance)
    make_plots('hierarchical: n=%s, m=%s, d=%s' % \
        (nclusters, method, distance), clusters, flat_data)
    
    
def k_means(flat_data, data, nclusters, method, distance):
    """ K-Means Clustering """
    clusterid, error, nfound = pc.kcluster(
                        flat_data.values(),
                        nclusters=nclusters,
                        mask=None,
                        weight=None,
                        transpose=0,
                        npass=100,
                        method=method,
                        dist=distance,
                        initialid=None)
    
    # load clusters into dictionary
    clusters = defaultdict(list)
    for i, j in zip(clusterid, data):
        clusters[i].append(j)
        
    return clusters


def hierarchical(flat_data, data, nclusters, method, distance):
    """ Hierarchical clustering """
    
    tree = pc.treecluster(data=flat_data.values(),
                       mask=None,
                       weight=None,
                       transpose=0,
                       method=method,
                       dist=distance,
                       distancematrix=None)
                       
    #for i in tree:
    #    print '%4s %4s   %2.2e' % (i.left, i.right, i.distance)
        
    clusterid = tree.cut(nclusters)

    clusters = defaultdict(list)
    for i, j in zip(clusterid, data):
        clusters[i].append(j)
        
    return clusters
    
            
def self_organizing_map(flat_data, data):
    """ """
    # Self-organizing maps
    clusterid, celldata = pc.somcluster(
                        data=flat_data.values(),
                        transpose=0,
                        nxgrid=5,
                        nygrid=5,
                        inittau=0.02,
                        niter=100,
                        dist='e')
                        
    # load clusters into dictionary
    clusters = defaultdict(list)
    for i, j in zip(clusterid, data):
        clusters[tuple(i)].append(j)
    
    make_plots('SOM (c=%s, m=%s, d=%s)' % (nclusters, method, distance),
                   clusters, flat_data)
                   
                       
def make_plots(title, nclusters, flat_data):
    """ Makes your plots """
    
    ma_plot(title, nclusters, flat_data)
    plot_clusters(title, nclusters, flat_data)
    lr_plot(title, nclusters, flat_data)

    
def print_clusters(clusters):
    """ Prints something that makes sense. """
    for i in clusters:
        print '    Cluster %s:' % i
        for j in sorted(clusters[i]):
            print '        %s' % (j)
            

def lr_plot(title, clusters, flat_data):
    """ log(2) ratio plot """
    
    fig = figure()
    ax = fig.add_subplot(111)
    
    ax.set_xlabel('log(2)[avg(cases, controls)]')
    ax.set_ylabel('log(2)[cases]+1/log(2)[controls]+1')
    ax.set_title(title)
    
    vectors = {}
    for c in clusters:
        color = colors[c]
        vectors[color] = []
        for g in clusters[c]:
            v = flat_data[g]
            j = math.log((v[0]+1)/(v[1]+1.0), 2)
            i = math.log((v[0] + v[1])/2.0, 2)
            vectors[color].append((i, j))

        plt.scatter([v[0] for v in vectors[color]], 
            [v[1] for v in vectors[color]], s=50, c=color, alpha=0.5)    

    show()
    

def ma_plot(title, clusters, flat_data):
    """ Plots data in an MA plot
    M = log(2)[case] - log(2)[control]
    A = .5(log(2)[case] + log(2)[control])
    """
    
    fig = figure()
    ax = fig.add_subplot(111)
    
    ax.set_xlabel('log(2)[cases] - log(2)[controls]')
    ax.set_ylabel('1/2(log(2)[cases] + log(2)[controls])')
    ax.set_title(title)
    
    vectors = {}
    for c in clusters:
        color = colors[c]
        vectors[color] = []
        for g in clusters[c]:
            v = (flat_data[g][0]+1, flat_data[g][1]+1)
            x = math.log(v[0], 2) - math.log(v[1], 2)
            y = (0.5)*(math.log(v[0], 2) + math.log(v[1], 2))
            vectors[color].append((x, y))

        plt.scatter([v[0] for v in vectors[color]],
                    [v[1] for v in vectors[color]],
                    s=50, c=color, alpha=0.5)  

    show()
        

def plot_clusters(title, clusters, flat_data):
    """ plots clustering output """
    
    fig = figure()
    ax = fig.add_subplot(111)

    ax.set_xlabel('# cases')
    ax.set_ylabel('# controls')
    ax.set_title(title)
    
    vectors = {}
    
    for c in clusters:
        color = colors[c]
        vectors[color] = []
        for g in clusters[c]:
            
            v = flat_data[g]
            vectors[color].append(v)
            
        plt.scatter([v[0] for v in vectors[color]], 
            [v[1] for v in vectors[color]], s=50, c=color, alpha=0.5)    
    
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
        if gene.count(';') > 0: continue
        gene = gene.split(',')[-1]
        
        # Let's try relative "expresion" levels
        # Ie. normalize at the row level
        
        data[gene] = { 'cases': [int(i) for i in values[4:]],
                       'controls': [int(i) for i in values[:4]] }
                       
    # We only want to consider {cases} versus {controls}
    flat_data = {}
    for k in data:
       i = data[k]
       flat_data[k] = [sum(i['cases'])/4.0, sum(i['controls'])/4.0]

    return data, flat_data

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
    
if __name__ == '__main__':
    main()