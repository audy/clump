# Clump

[Austin G. Davis-Richardson](harekrishna@gmail.com)  

Quantitative Ontologies -> Biologically Interesting Inferences

## Goal

To investigate the usefulness of various clustering algorithms and distance
metrics on a dataset made from Illumina sequencing reads and classified with
the SEED database into ontology subsystem trees.

## Distance Metric

  - Δreads
  - distance in subsystem tree (if possible)
  - and both: Δreads * tree distance

## Clustering Algorithms

I plan on implementing the following:

  - [k-Means Clustering][1]
  - [Hierarchical Clustering][2]
  - [Expectation Maximization][3]

## Dataset

I have a dataset that looks like this:

    # 1	i+1	..	n	Ontology
    100	20	..	90	System
    50	10	..	30	System; Subsystem 1
    50	10	..	60	System; Subsystem 2
    25	1	..	50	System; Subsystem 2; Subsubsystem 1
    25	9	..	10	System; Subsystem 2; Subsubsystem 2

(The numbers are read counts similar to expression data on a microarray,
notice they add up)

Subsystems are generated from the [SEED][4] database
using tools created prior to this project.

## Methods

I will use the following:

  - [Python][5]
  - [PyCluster][6] which is a python wrapper for the
    [C Clustering Library][7] (PDF).
  - Possibly [Numpy][8], [SciPy][10] and [MatPlotLib][9]
  
## Relavent Papers

(Just for starters)

  -  A k-means clustering algorithm, JA Hartigan, MA Wong - JR Stat. Soc., Ser. C, 1979
  - 
  
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