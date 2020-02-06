# Trie-based paradigm extraction

This repository contains code for a work-in-progress on unsupervised extraction of paradigms from text corpora.

The algorithm consists of two steps:

1. Construct a trie of all words in the corpus. Using the trie's enhanced API, extract counts of all suffixes for all branching prefixes. E.g., given the following input:
    ```
    cat
    car
    call
    caledonian
    calling
    come
    dawn
    damn
    drill
    dry
    ```
    the output is
    ```json
    {"c": {"aledonian": 1, "all": 1, "alling": 1, "ar": 1, "at": 1, "ome": 1},
     "ca": {"ledonian": 1, "ll": 1, "lling": 1, "r": 1, "t": 1},
     "cal": {"edonian": 1, "l": 1, "ling": 1},
     "call": {"": 1, "ing": 1},
     "d": {"amn": 1, "awn": 1, "rill": 1, "ry": 1},
     "da": {"mn": 1, "wn": 1},
     "dr": {"ill": 1, "y": 1}}
    ```
   
2. Convert this to a prefix–suffix co-occurrence matrix (tried using Pandas, but this eats all the memory and gets the process killed). Select suffixes that are frequent enough and have a high enough entropy (grammatical suffixes should be non-restrictive as to their host).

3. Identify suffixes that tend to co-occur with different prefixes using some distance metric (modified Chi-square, Fisher's exact test, etc., I started with arccosine-transformed correlations).

4. Clusterise suffixes based on this distance measure. Paradigms should emerge as coherent clusters.

Reversing all words can be used to test for prefix-based paradigms.