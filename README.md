# Multi-seq-Alignment

In almost all aspects of computational biology, sequence alignment is one of the very first steps in data processing. Aligning sequences allows for accurate comparison of DNA or protein sequences. By comparing sequences, biologists can find common structures and functionalities between them, and further analyze their evolutionary relationship.

Basic pairwise sequence alingment can be computed using the Needleman-Wunsch Algorithm (NW), though some more modern approaches have explored using Markov Models. The NW algorithm is explained in depth here: https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

There are several ways to do multiple sequence alignment, but this project uses the most rudimentary version. 

## Instructions for Use
coming soon!

## How it Works

### Modifications to the Needleman-Wunsch
In this implementation, the NW algorithm has been modified to accept sequence profiles instead of sequences. A sequence profile is just a probability table of the possible observations at each index:

[insert image here]

This allows the NW algorithm to account for multiple sequences at a time by using the following calculation:

$$Score_{x} = \sum_{i=1}^n \sum_{j=1}^m P_x(i) * P_x(j) * S(i,j)$$

where $x$ is the index, $n$ and $m$ are the possible observable states in profile 1 and 2, $P_x(i)$ and $P_x(j)$ are the probabilities of observing $i$ or $j$ at position x in profile 1 and 2, and $S(i,j)$ is the scoring function for a match between $i$ and $j$

### Aligning Multiple Sequences
This implementation uses a graph like structure to align multiple sequences.

At the start, each node object in the graph contains a profile made of one sequence (i.e. one state has a 100% chance of being observed at each index).
The nodes are connected by edge objects, each of which contain the results of a NW algorithm using the profiles from the two nodes that it connects. Most importantly, they contain a final score for the alignment, as well as data detailing how each profile must be modified when aligned. 

[Insert Image here]

At every iteration, the edge with the highest score is found. The two node objects that the edge connects are deleted along with any connections made with other nodes. A new node is then created using the modifiation data from the edge, and the profiles from the two nodes. 

The new node object is inserted into the graph, and the edges connecting it to all other nodes are recalculated.

[Insert Image here]

In the final iteration, only one node will remain, containg the properly aligned sequences. 
