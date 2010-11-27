# Clump

Clump is a term derived from the latin _clumpus_ which means to shake one's
belly fat in an amusing way before finding treasure.

[Austin G. Davis-Richardson](harekrishna@gmail.com)  

## Goal

To investigate the usefulness of various clustering algorithms and distance
metrics on a dataset made from Illumina sequencing reads and classified with the SEED database into ontology subsystem trees.

## Description of Ontology classification Pipeline

Unpublished, so I can't talk about it yet. In a nutshell, genes are found and classified from Illumina pyrosequencing reads taken from human stool samples. Gene annotation is based on similiarity to [The SEED Database][4].

## Requirements

To run these scripts you need:

   - [MatPlotLib][9]
   - [Numerical Python][8]
   - [Scientific Python][10]
   - [PyCluster][6]

Getting all of these packages installed on your system can be tricky. I recommend first installing [Python 2.6.6][5] from source into your `/usr/local/bin` directory and setting your environment variable `PYTHONPATH` to `/usr/local/lib/python2.6/`. Then, download and install all of the above packages from source (do not use the installers). My success using this method varied even on systems with the same OS and compiler versions.

If I find my methods to be useful, I may release this project in the form of a VirtualBox image to make things easier.

## Clustering

I am testing the algorithms available in PyCluster, which is a python wrapper for the C clustering library.

### Distance Computation

  - Unweighted (Absolute) Pearson Correlation
  - Uncentered Pearson Correlation
  - Kendall's Tau
  - Euclidean Distance

### Clustering Algorithms

   - Hierarchical clustering
   - _k_-means clustering
   - Principal Component Analysis

## Dataset

These scripts take a dataset that looks like this:
If there is a `#` present in the system annotation, the gene counts are overlooked.

    # 1	i+1	..	n	Ontology
    100	20	..	90	System
    50	10	..	30	System; Subsystem 1
    50	10	..	60	System; Subsystem 2
    25	1	..	50	System; Subsystem 2; Subsubsystem 1
    25	9	..	10	System; Subsystem 2; Subsubsystem 2

(The numbers are read counts similar to expression data on a microarray,
notice they add up)

  
## Relavent Papers

Just for starters...

  - Hartigan, J. A.; Wong, M. A. (1979). "Algorithm AS 136: A K-Means
    Clustering Algorithm". Journal of the Royal Statistical Society
  - Ward, Joe H. (1963). "Hierarchical Grouping to Optimize an Objective
    Function". Journal of the American Statistical Association
  - Jain, MN Murty, PJ Flynn (1999). "Data clustering: a review". ACM
    computing surveys
  - Moon, T.K. (1996). "The Expectation Clustering Algorithm". Signal
    Processing Magazine, IEEE    
  
[1]: http://en.wikipedia.org/wiki/K-means_clustering
[2]: http://en.wikipedia.org/wiki/Hierarchical_clustering
[3]: http://en.wikipedia.org/wiki/Expectation-maximization_algorithm
[4]: http://www.theseed.org
[5]: http://www.python.org
[6]: http://pypi.python.org/pypi/Pycluster
[7]: http://bonsai.hgc.jp/~mdehoon/software/cluster/cluster.pdf
[8]: http://numpy.scipy.org
[9]: http://matplotlib.sourceforge.net/
[10]: http://www.scipy.org