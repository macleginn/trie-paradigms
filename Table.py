"""A helper module that provides a function to create a co-occurrence table for
a corpus using Trie.py"""

import re
import string
from collections import Counter
from math import log2

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


def corpus2table(data_path, table_path=None, lang=None):
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
    sorted_counts = suffix_counts.most_common(300)
    suffixes = [el[0] for el in sorted_counts]
    freqs = [el[1] for el in sorted_counts]

    d = pd.DataFrame(index = prefixes, columns = suffixes, dtype = int).fillna(0)
    for prefix, suffix_counts_for_prefix in prefix_suffix_tree.items():
        print(prefix)
        for suffix, count in suffix_counts_for_prefix.items():
            if suffix in d.columns:
                d.loc[prefix,suffix] = count
    
    print('Dataframe constructed')

    entropies = d.apply(entropy)

    if lang is not None:
        # Regress entropies on log frequencies
        plt.figure(figsize=(16,10))
        plt.scatter(np.log(freqs), entropies, marker = 'o')
        plt.savefig(f'/home/macleginn/Analyses/bible-tables/img/entropies_log_freqs_{lang}.png')
    
    cutoff = np.quantile(entropies, 0.9)    
    d = d.loc[:,entropies > cutoff]

    print('Columns selected')
    
    if table_path is not None:
        d.to_csv(table_path)
        
    return d


def corpora2dict(path):
    data_dict = {
        'log_frequency': [],
        'entropy': [],
        'doculect': []
    }
    trie = Trie()
    doculect = path.split('/')[-1].split('.')[0]
    print(doculect)
    with open(path, 'r', encoding='utf-8') as inp:
        for line in inp:
            words = word_tokenize(line)
            for w in words:
                w = non_word_pattern.sub('', w)
                if not w:
                    continue
                trie.insert(f'{w.lower()}#')
    prefix_suffix_tree = trie.get_prefix_suffix_tree()
    prefixes = sorted(prefix_suffix_tree.keys())
    suffix_counts = Counter()
    for v in prefix_suffix_tree.values():
        for k, count in v.items():
            suffix_counts[k] += count
                
    # Take N most common suffixes
    sorted_counts = suffix_counts.most_common(300)
    suffixes = [el[0] for el in sorted_counts]
    freqs = [el[1] for el in sorted_counts]

    # Construct an intermediate data frame to compute entropies
    d = pd.DataFrame(index = prefixes, columns = suffixes, dtype = int).fillna(0)
    for prefix, suffix_counts_for_prefix in prefix_suffix_tree.items():
        for suffix, count in suffix_counts_for_prefix.items():
            if suffix in d.columns:
                d.loc[prefix,suffix] = count

    entropies = d.apply(entropy)
    for f, e in zip(np.log(freqs), entropies):
        data_dict['doculect'].append(doculect)
        data_dict['log_frequency'].append(f)
        data_dict['entropy'].append(e)

    return data_dict


if __name__ == '__main__':
    corpus2table('test_data/duc.txt', 'test_data/duc.csv', False)
