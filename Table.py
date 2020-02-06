"""A helper module that provides a function to create a co-occurrence table for
a corpus using Trie.py"""

import re
import string
from collections import Counter
from math import log2

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize

from Trie import Trie

# TODO: a better word filter
non_word_pattern = re.compile(f'(\\d|[{string.punctuation}—])+')


def entropy(vector):
    total = sum(vector)
    entropy = 0
    for el in vector:
        if el > 0:
            entropy += -1 * el/total * log2(el/total)
    return entropy


def corpus2table(data_path, table_path=None):
    trie = Trie()

    with open(data_path, 'r', encoding='utf-8') as inp:
        for line in inp:
            words = word_tokenize(line)
            for w in words:
                w = non_word_pattern.sub('', w)
                if not w:
                    continue
                trie.insert(f'{w.lower()}#')
    prefix_suffix_tree = trie.get_prefix_suffix_tree()

    print('Tree constructed')

    prefixes = sorted(prefix_suffix_tree.keys())
    suffix_counts = Counter()
    for v in prefix_suffix_tree.values():
        for k, count in v.items():
            suffix_counts[k] += count

    # Take N most common suffixes
    sorted_counts = suffix_counts.most_common(1000)
    suffixes = [el[0] for el in sorted_counts]

    d = pd.DataFrame(index = prefixes, columns = suffixes, dtype = int).fillna(0)
    for prefix, suffix_counts_for_prefix in prefix_suffix_tree.items():
        print(prefix)
        for suffix, count in suffix_counts_for_prefix.items():
            if suffix in d.columns:
                d.loc[prefix,suffix] = count
    
    print('Dataframe constructed')

    entropies = d.apply(entropy)
    cutoff = np.quantile(entropies, 0.9)
    d = d.loc[:,entropies > cutoff]

    print('Columns selected')
    
    if table_path is not None:
        d.to_csv(table_path)
        
    return d


if __name__ == '__main__':
    corpus2table('test_data/duc.txt', 'test_data/duc.csv', False)
