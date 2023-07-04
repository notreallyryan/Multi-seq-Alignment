# Multi-seq-Alignment

In almost all aspects of computational biology, sequence alignment is one of the very first steps in data processing. Aligning sequences allows for accurate comparison of DNA or protein sequences. By comparing sequences, biologists can find common structures and functionalities between them, and further analyze their evolutionary relationship.

Basic pairwise sequence alingment can be computed using the Needleman-Wunsch Algorithm (NW), though some more modern approaches have explored using Markov Models. The NW algorithm is explained in depth here: https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

There are several ways to do multiple sequence alignment, but this project uses the most rudimentary version. 

## Instructions for Use
coming soon!

## How it Works
In this implementation, the NW algorithm has been modified to accept sequence profiles instead of sequences. A sequence profile is just a probability table of the possible observations at each index:

[insert image here]

This allows the NW algorithm to account for multiple sequences at a time by using the following calculation:

$$Score_{x} = \sum_{i=1}^n \sum_{j=1}^n P_x(i) * P_x(j) * S(i,j)$$

