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
                        nclusters=5,
                        mask=None,
                        weight=None,
                        transpose=0,
                        npass=1,
                        method='a',
                        dist='e',
                        initialid=None)
                                    
    # Load clusters into dictionary
    clusters = defaultdict(list)
    for i, j in zip(clusterid, data):
        clusters[i].append(j)

    
    # Print output so that it makes sense
    #print_clusters(clusters)
    
    lr_plot(clusters, flat_data)
    plot_clusters(clusters, flat_data)
    
    
def print_clusters(clusters):
    """ Prints something that makes sense. """
    for i in clusters:
        print '    Cluster %s:' % i
        for j in sorted(clusters[i]):
            print '        %s' % (j)
            

def lr_plot(clusters, flat_data):
    """ log(2) ratio plot """
    
    fig = figure()
    ax1 = fig.add_subplot(111)
    
    colors = ['b', 'y', 'g', 'r', 'c']
    
    vectors = {}
    for c in clusters:
        color = colors[c]
        vectors[color] = []
        for g in clusters[c]:
            v = flat_data[g]
            j = math.log((v[0]+1)/(v[1]+1.0), 2)
            i = v[0]
            vectors[color].append((i, j))

        plt.scatter([v[0] for v in vectors[color]], 
            [v[1] for v in vectors[color]], s=50, c=color, marker='s')    

    show()
    

def ma_plot(clusters, flat_data):
    """ Plots data in an MA plot
    M = log(2)[case] - log(2)[control]
    A = .5(log(2)[case] + log(2)[control])
    """
    

    vectors = []    
    fig = figure()
    ax1 = fig.add_subplot(111)

    for c in clusters:
        for g in clusters[c]:
            v = (flat_data[g][0]+1, flat_data[g][1]+1)
            x = math.log(v[0], 2) - math.log(v[1], 2)
            y = (0.5)*(math.log(v[0], 2) + math.log(v[1], 2))
            vectors.append((x, y))
            
    plt.scatter([v[0] for v in vectors], [v[1] for v in vectors],
        s=20, color='r', marker='s')
        
    show()

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
            [v[1] for v in vectors[color]], s=50, c=color, marker='s')    
    
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
        #if gene.count(';') != 3: continue
        gene = gene.split(',')[-1]
        
        # Let's try relative "expresion" levels
        # Ie. normalize at the row level
        
        data[gene] = { 'cases': [int(i) for i in values[4:]],
                       'controls': [int(i) for i in values[:4]] }

    return data

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